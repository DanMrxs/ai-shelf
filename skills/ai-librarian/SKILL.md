---
name: ai-librarian
description: Cataloga skills, plugins, servidores MCP e repositórios na estante pessoal ai-shelf. Use ao receber links do GitHub, comandos de instalação ou ideias de prompts e regras autorais, e quando Daniel pedir para salvar na estante, adicionar uma skill, catalogar ou consultar a biblioteca.
---

# AI Librarian

Abra o repositório em `C:/Users/danie/projects/ai-shelf`. O `catalog.json` é a fonte dos índices. Em consultas sobre o que já existe, pesquise o catálogo e responda sem editar.

## Inspecionar

Para URLs, leia o README e a estrutura do repositório. Identifique a finalidade em uma linha, a stack e o método oficial de instalação. Para comandos recebidos, confira o pacote e a origem antes de registrá-los. A instalação de ferramentas de terceiros é uma ação separada da catalogação. Para prompts ou regras, identifique a finalidade e procure uma skill autoral equivalente.

## Classificar

Escolha uma categoria pelo uso principal:

- `01-engenharia-e-dev`: código, arquitetura, testes, CLI e IDE.
- `02-automacao-e-workflows`: n8n, pipelines, webhooks, MCP e orquestração.
- `03-pesquisa-e-scraping`: pesquisa, extração de dados, browser agents e OSINT.
- `04-conteudo-e-midia`: vídeo, Remotion, avatares, copywriting e design.
- `05-negocios-e-operacoes`: vendas, propostas, ERP, finanças e gestão.

Use `validado` com evidência de instalação ou teste no ambiente de Daniel. Use `radar` para descobertas que aguardam avaliação.

## Registrar e sincronizar

1. Para uma skill autoral, crie ou atualize `skills/<slug>/SKILL.md` usando o padrão Agent Skills com `name` e `description` no YAML. O nome coincide com o slug da pasta.
2. Vincule a pasta canônica nos diretórios `~/.claude/skills`, `~/.gemini/skills`, `~/.codex/skills` e `~/.gemini/config/skills` (Antigravity). Use symlinks ou, no Windows, junctions de diretório. Se um vínculo já apontar para a pasta certa, reutilize-o. Preserve entradas preexistentes com outros destinos.
3. Compare nome, slug e URL com o catálogo antes de editar. Atualize uma entrada equivalente quando houver nova evidência. Preencha `name`, `slug`, `category`, `status`, `type`, `description`, `url`, `comando_install`, `local_path` e `tags`. Use uma linha na descrição e hífens simples. Use strings vazias para campos de texto que não se aplicam. Registre caminhos de configuração e referências públicas sem copiar credenciais.
4. Execute `python scripts/sync_library.py` na raiz do repositório. Confira o README, a coleção da categoria e a nota correspondente em `C:/Users/danie/Documents/Obsidian/2ndBrain/AI-Shelf`.
5. Se houver remote Git configurado, confira o diff e execute `git add .` e `git commit -m "chore(shelf): add <nome-do-item>"` para as mudanças da estante. Preserve mudanças alheias à tarefa, usando staging seletivo se estiverem presentes. A publicação no remote segue a autorização da conversa.

Confirme o resultado em três linhas. Registre falhas ou etapas pendentes quando houver.

```text
Item: <nome>
Categoria: <categoria> | Status: <✅ Validado ou 🔭 Radar>
Sync: <resultado Git> | <resultado Obsidian>
```