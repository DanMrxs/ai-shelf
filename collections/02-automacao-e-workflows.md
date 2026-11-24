# 02-automacao-e-workflows: Automação e Workflows

| Item / Repo | Status | O que resolve | Instalação / Caminho |
|---|---|---|---|
| 2ndbrain-rag | ✅ Validado | RAG MCP server para o vault Obsidian 2ndBrain | `python ~/tools/brain_rag_mcp.py`<br>`~/tools/brain_rag_mcp.py` |
| [AI Librarian](../skills/ai-librarian/SKILL.md) | ✅ Validado | Cataloga ferramentas e sincroniza a estante Git com o Obsidian. | `skills/ai-librarian/SKILL.md` |
| Cloudflare API | ✅ Validado | Consulta e gerencia recursos da conta Cloudflare por MCP. | `~/.codex/config.toml` |
| cloudflare-email-service | ✅ Validado | Email transacional via Cloudflare: sending, routing, SPF/DKIM | `Antigravity built-in`<br>`~/.agents/skills/cloudflare-email-service` |
| context7 | ✅ Validado | Upstash Context7: documentacao contextual on-demand via MCP | `npm install @upstash/context7-mcp`<br>`~/.claude/mcp.json` |
| Docker MCP Gateway | ✅ Validado | Conecta o cliente aos servidores MCP registrados no Docker. | `~/.codex/config.toml` |
| Email Agent More AI Less Cost | ✅ Validado | Integra a caixa More AI Less Cost ao agente de e-mail. | `~/.codex/config.toml` |
| Email Agent ProHeroSports | ✅ Validado | Integra a caixa ProHeroSports ao agente de e-mail. | `~/.codex/config.toml` |
| [email-agent](https://github.com/DanMrxs/email-agent) | ✅ Validado | Agente MCP de email: send/receive via Python IMAP/SMTP | `cd ~/Documents/email-agent && pip install -e .`<br>`~/Documents/email-agent` |
| graphify | ✅ Validado | Transforma codigo/docs/URLs em knowledge graphs com GraphRAG | `Antigravity built-in`<br>`~/.agents/skills/graphify` |
| hermes-agent | ✅ Validado | Agente multi-plataforma com skills, cron, hooks e memorias (WSL) | `WSL: ~/.hermes/`<br>`/home/danie/.hermes/hermes-agent` |
| JSON Canvas | ✅ Validado | Monta mapas em JSON Canvas com nós, grupos e conexões. | `~/.agents/skills/json-canvas` |
| loop-engineering | ✅ Validado | Loops autonomos de agentes com self-healing e maker/checker split | `Antigravity built-in`<br>`~/.agents/skills/loop-engineering` |
| [mcp-servers-repo](https://github.com/modelcontextprotocol/servers) | ✅ Validado | Repositorio oficial de MCP Servers (referencia) | `git clone https://github.com/modelcontextprotocol/servers`<br>`~/mcp-servers/mcp-servers-repo` |
| n8n Expression Syntax | ✅ Validado | Valida e corrige expressões de workflows n8n. | `~/.agents/skills/n8n-expression-syntax` |
| n8n MCP | ✅ Validado | Acessa os workflows e as execuções da instância n8n. | `~/.codex/config.toml` |
| n8n Node Configuration | ✅ Validado | Configura nós n8n conforme a operação e seus argumentos. | `~/.agents/skills/n8n-node-configuration` |
| n8n Validation Expert | ✅ Validado | Interpreta erros de validação em workflows n8n. | `~/.agents/skills/n8n-validation-expert` |
| n8n-code-javascript | ✅ Validado | JavaScript em Code nodes do n8n: $input, $json, HTTP, DateTime | `Antigravity built-in`<br>`~/.agents/skills/n8n-code-javascript` |
| n8n-code-python | ✅ Validado | Python em Code nodes do n8n: _input, _json, standard library | `Antigravity built-in`<br>`~/.agents/skills/n8n-code-python` |
| n8n-mcp-tools-expert | ✅ Validado | Uso experto de ferramentas MCP no n8n: search, validate, templates | `Antigravity built-in`<br>`~/.agents/skills/n8n-mcp-tools-expert` |
| n8n-workflow-patterns | ✅ Validado | Padroes arquiteturais para workflows n8n (webhook, DB, AI agents) | `Antigravity built-in`<br>`~/.agents/skills/n8n-workflow-patterns` |
| Obsidian Bases | ✅ Validado | Monta visualizações e filtros nas bases do Obsidian. | `~/.agents/skills/obsidian-bases` |
| Obsidian Markdown | ✅ Validado | Edita notas do Obsidian com propriedades, wikilinks e embeds. | `~/.agents/skills/obsidian-markdown` |
| obsidian-cli | ✅ Validado | CLI para interagir com vaults Obsidian: notes, tasks, search, plugins | `Antigravity built-in`<br>`~/.agents/skills/obsidian-cli` |
| [obsidian-mcp-server](https://github.com/DanMrxs/obsidian-mcp-server) | ✅ Validado | MCP Server customizado para Obsidian (fork com 20+ skills) | `cd ~/mcp-servers/obsidian && npm install && npm run build`<br>`~/mcp-servers/obsidian` |
| orca-cli | ✅ Validado | Orca worktrees, terminals, repos, automations e browser | `Antigravity built-in`<br>`~/.agents/skills/orca-cli` |
| orchestration | ✅ Validado | Coordenacao de workers Orca: dispatch, heartbeats, DAGs, decision gates | `Antigravity built-in`<br>`~/.agents/skills/orchestration` |
| Ruflo MCP | ✅ Validado | Expõe mecanismos de coordenação, memória e estado de agentes. | `~/.codex/config.toml` |
| Sequential Thinking | ✅ Validado | Organiza raciocínio iterativo em etapas. | `~/.codex/config.toml` |
| sequential-thinking | ✅ Validado | Raciocinio estruturado step-by-step para problemas complexos | `Antigravity built-in`<br>`~/.agents/skills/sequential-thinking` |
| Supabase MCP | ✅ Validado | Fornece acesso aos projetos e bancos Supabase. | `~/.gemini/antigravity/mcp_config.json` |
| [claude-mem](https://github.com/thedotmack/claude-mem) | 🔭 Radar | Plugin de memoria persistente para Claude | `git clone git@github.com:thedotmack/claude-mem.git`<br>`~/.claude/plugins/marketplaces/thedotmack` |
| [kepano-obsidian-skills](https://github.com/kepano/obsidian-skills) | 🔭 Radar | Skills Obsidian por Kepano: defuddle, json-canvas, bases, cli, markdown | `git clone https://github.com/kepano/obsidian-skills`<br>`~/mcp-servers/kepano-skills` |

[Voltar ao índice](../README.md)
