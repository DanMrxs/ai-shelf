#!/usr/bin/env python3
"""Valida o catálogo e regenera as páginas do ai-shelf e seu espelho no Obsidian."""

import argparse
from contextlib import contextmanager
from datetime import date
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit

REPO = Path(__file__).resolve().parents[1]
DEFAULT_VAULT = Path.home() / "Documents" / "Obsidian" / "2ndBrain"
CATEGORIES = {
    "01-engenharia-e-dev": "Engenharia e Dev",
    "02-automacao-e-workflows": "Automação e Workflows",
    "03-pesquisa-e-scraping": "Pesquisa e Scraping",
    "04-conteudo-e-midia": "Conteúdo e Mídia",
    "05-negocios-e-operacoes": "Negócios e Operações",
}
STATUS = {"validado": "✅ Validado", "radar": "🔭 Radar"}
TYPES = {"skill", "repo", "tool", "plugin", "mcp-server"}
FIELDS = ("name", "slug", "category", "status", "type", "url", "comando_install",
          "local_path", "description")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MARKER = "ai_shelf_managed: true"


def catalog() -> list[dict]:
    items = json.loads((REPO / "catalog.json").read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError("catalog.json deve conter uma lista de itens")
    seen = {"slug": set(), "name": set(), "url": set()}
    for index, item in enumerate(items, start=1):
        label = f"catalog.json, item {index}"
        if not isinstance(item, dict):
            raise ValueError(f"{label}: esperado um objeto")
        for field in FIELDS:
            value = item.get(field)
            if not isinstance(value, str) or value.strip() != value or len(value.splitlines()) > 1:
                raise ValueError(f"{label}: '{field}' deve ser texto de uma linha")
        label += f" ({item['slug']})"
        tags = item.get("tags")
        if not isinstance(tags, list) or any(
            not isinstance(tag, str) or not tag.strip() or len(tag.splitlines()) > 1 for tag in tags
        ):
            raise ValueError(f"{label}: 'tags' deve ser uma lista de textos")
        if not SLUG.fullmatch(item["slug"]) or not item["name"] or not item["description"]:
            raise ValueError(f"{label}: nome, slug ou descrição inválido")
        if item["category"] not in CATEGORIES or item["status"] not in STATUS or item["type"] not in TYPES:
            raise ValueError(f"{label}: categoria, status ou tipo inválido")
        if any(char in item["name"] + item["description"] for char in "–—"):
            raise ValueError(f"{label}: use hífens simples no nome e na descrição")
        url = item["url"]
        normalized_url = ""
        if url:
            parsed = urlsplit(url)
            if (
                parsed.scheme not in {"https", "http"} or not parsed.hostname or parsed.username
                or parsed.password or any(char.isspace() for char in url)
            ):
                raise ValueError(f"{label}: URL HTTP(S) sem credenciais esperada")
            path = parsed.path.rstrip("/")
            query = parsed.query
            if parsed.hostname.casefold() == "github.com" and len(path.strip("/").split("/")) == 2:
                path = path.casefold().removesuffix(".git")
                query = ""
            normalized_url = (parsed.netloc.casefold(), path, query)
        identities = {"slug": item["slug"], "name": " ".join(item["name"].casefold().split()),
                      "url": normalized_url}
        for field, identity in identities.items():
            if identity in seen[field]:
                raise ValueError(f"{label}: {field} duplicado")
            if identity:
                seen[field].add(identity)
    return items


def authored_skills() -> dict[str, str]:
    skills = {}
    for path in sorted((REPO / "skills").glob("*/SKILL.md")):
        slug = path.parent.name
        text = path.read_text(encoding="utf-8")
        frontmatter, delimiter, body = text[4:].partition("\n---\n")
        if (
            not SLUG.fullmatch(slug) or len(slug) > 64 or not text.startswith("---\n")
            or not delimiter or not body.strip()
            or not re.search(rf"""^name:[ \t]*['"]?{re.escape(slug)}['"]?[ \t]*$""", frontmatter, re.M)
            or not re.search(r"^description:[ \t]*\S", frontmatter, re.M)
        ):
            raise ValueError(f"{path}: SKILL.md requer name, description e conteúdo")
        skills[slug] = body.lstrip()
    return skills


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def code(text: str) -> str:
    backtick = chr(96)
    fence = backtick * (1 + max((len(run) for run in re.findall(backtick + "+", text)), default=0))
    padding = " " if text.startswith(backtick) or text.endswith(backtick) else ""
    return f"{fence}{padding}{text}{padding}{fence}"


def table(items: list[dict], skill_links: dict[str, str]) -> str:
    if not items:
        return "_Nenhum item._"
    lines = ["| Item / Repo | Status | O que resolve | Instalação / Caminho |", "|---|---|---|---|"]
    for item in sorted(items, key=lambda row: (row["status"] != "validado", row["name"].casefold())):
        name = cell(item["name"])
        url = item["url"].replace("(", "%28").replace(")", "%29").replace("|", "%7C")
        link = skill_links.get(item["slug"])
        if link:
            name = link
        elif url:
            name = f"[{name}]({url})"
        locations = [code(cell(value)) for value in (item["comando_install"], item["local_path"]) if value]
        action = "<br>".join(locations) or "-"
        lines.append(f"| {name} | {STATUS[item['status']]} | {cell(item['description'])} | {action} |")
    return "\n".join(lines)


def stats(items: list[dict]) -> tuple[int, int, int]:
    return (
        sum(item["status"] == "validado" for item in items),
        sum(item["status"] == "radar" for item in items),
        sum(item["type"] == "mcp-server" and item["status"] == "validado" for item in items),
    )


def overview(title: str, items: list[dict], links: dict[str, str]) -> str:
    validated, radar, mcps = stats(items)
    return "\n\n".join((
        f"# {title}",
        f"{validated} validados · {radar} no Radar · {mcps} MCPs ativos",
        "## Radar (Fila de Testes)",
        table([item for item in items if item["status"] == "radar"], links),
        "## Servidores MCP Ativos",
        "Servidores habilitados nas configurações dos clientes.",
        table([item for item in items if item["type"] == "mcp-server" and item["status"] == "validado"], links),
    ))


def note(title: str, body: str, related: list[str], kind: str = "reference") -> str:
    return (
        f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\n"
        f"type: {'project' if kind == 'active' else 'source'}\n"
        f"status: {kind}\ntags: [ai-shelf, curadoria]\nupdated: {date.today().isoformat()}\n"
        f"related: {json.dumps(related, ensure_ascii=False)}\n{MARKER}\n---\n\n{body.rstrip()}\n"
    )


def render(items: list[dict], skills: dict[str, str], shelf: Path) -> tuple[dict, dict]:
    names = {item["slug"]: item["name"] for item in items}
    git_links = {slug: f"[{cell(names.get(slug, slug))}](skills/{slug}/SKILL.md)" for slug in skills}
    vault_links = {
        slug: rf"[[AI-Shelf/Skills/{slug}\|{cell(names.get(slug, slug))}]]" for slug in skills
    }
    readme = [overview("AI Shelf", items, git_links)]
    category_links = []
    git_files = {}
    vault_files = {}
    master = "[[AI-Shelf/AI-Shelf-MOC]]"
    collection_links = {slug: link.replace("](skills/", "](../skills/") for slug, link in git_links.items()}
    for category, label in CATEGORIES.items():
        rows = [item for item in items if item["category"] == category]
        readme.extend((f"## [{label}](collections/{category}.md)", table(rows, git_links)))
        title = f"{category}: {label}"
        git_files[REPO / "collections" / f"{category}.md"] = (
            f"# {title}\n\n{table(rows, collection_links)}\n\n[Voltar ao índice](../README.md)\n"
        )
        category_link = f"AI-Shelf/AI-Shelf-{category}"
        category_links.append((f"[[{category_link}]]", f"- [[{category_link}|{label}]]"))
        vault_files[shelf / f"AI-Shelf-{category}.md"] = note(
            title, f"# {title}\n\n{table(rows, vault_links)}\n\n{master}", [master]
        )

    moc = [overview("AI Shelf MOC", items, vault_links), "## Categorias",
           "\n".join(display for _, display in category_links)]
    if skills:
        readme.extend(("## Skills autorais", "\n".join(f"- {link}" for link in git_links.values())))
        moc.extend(("## Skills autorais",
                    "\n".join(f"- [[AI-Shelf/Skills/{slug}|{names.get(slug, slug)}]]" for slug in skills)))
    for slug, body in skills.items():
        vault_files[shelf / "Skills" / f"{slug}.md"] = note(
            names.get(slug, slug), f"{body.rstrip()}\n\n{master}", [master]
        )

    git_files[REPO / "README.md"] = "\n\n".join(readme) + "\n"
    vault_files[shelf / "AI-Shelf-MOC.md"] = note(
        "AI Shelf MOC", "\n\n".join(moc),
        [link for link, _ in category_links] + [f"[[AI-Shelf/Skills/{slug}]]" for slug in skills], kind="active"
    )
    return git_files, vault_files


def managed(text: str) -> bool:
    return text.startswith("---\n") and MARKER in text[4:].partition("\n---\n")[0].splitlines()


def verify_destination(path: Path, root: Path) -> None:
    if path.is_symlink() or not path.parent.resolve().is_relative_to(root):
        raise ValueError(f"Destino fora do diretório previsto: {path}")


@contextmanager
def sync_lock():
    path = REPO / ".tmp" / "sync.lock"
    path.parent.mkdir(exist_ok=True)
    with path.open("a+b") as lock:
        if os.name == "nt":
            import msvcrt
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        yield


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent, delete=False) as temp:
        temporary = Path(temp.name)
        try:
            temp.write(content)
            temp.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def sync(vault: Path, dry_run: bool) -> None:
    if not vault.is_dir():
        raise ValueError(f"Vault não encontrado: {vault}")
    shelf = vault.resolve() / "AI-Shelf"
    items = catalog()
    git_files, vault_files = render(items, authored_skills(), shelf)
    writes = {}
    for path, text in (git_files | vault_files).items():
        is_vault = path in vault_files
        verify_destination(path, shelf if is_vault else REPO)
        previous = path.read_text(encoding="utf-8") if path.exists() else None
        if is_vault and previous is not None:
            if not managed(previous):
                raise ValueError(f"A nota de destino já existe e não é gerenciada pelo ai-shelf: {path}")
            without_date = re.compile(r"^updated: \d{4}-\d{2}-\d{2}$", re.M)
            if without_date.sub("updated:", previous, count=1) == without_date.sub("updated:", text, count=1):
                continue
        if text != previous:
            writes[path] = text

    stale = []
    for path in (shelf / "Skills").glob("*.md"):
        if path in vault_files:
            continue
        verify_destination(path, shelf)
        if managed(path.read_text(encoding="utf-8")):
            stale.append(path)
    if not dry_run:
        for path, text in writes.items():
            write_file(path, text)
        for path in stale:
            path.unlink()

    validated, radar, mcps = stats(items)
    action = "Simulação" if dry_run else "Sync concluído"
    print(f"{action}: {validated} validados, {radar} no Radar, {mcps} MCPs ativos.")
    print(f"Git: {len(git_files)} arquivos | Obsidian: {len(vault_files)} notas | "
          f"{len(writes)} atualizações | {len(stale)} notas geradas obsoletas")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=DEFAULT_VAULT, help="Pasta do vault Obsidian")
    parser.add_argument("--dry-run", action="store_true", help="Valida e exibe o plano sem gravar arquivos")
    args = parser.parse_args()
    try:
        if args.dry_run:
            sync(args.vault, dry_run=True)
        else:
            with sync_lock():
                sync(args.vault, dry_run=False)
    except (OSError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())