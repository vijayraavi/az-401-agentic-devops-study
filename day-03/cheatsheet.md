# Day 3 Cheat Sheet: Agentic collaboration, MCP servers, webhooks & service hooks (Domain 1, 15–20%)

**Requirements (guide) vs restrictions (enforce).** Instructions are not a permission boundary. Restrict **tools** instead ([VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)).

| File | Rules |
|---|---|
| `.github/copilot-instructions.md` | Repo-wide. Priority: personal > repository > organization, all sent ([source](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)) |
| `.github/instructions/NAME.instructions.md` | Front matter `applyTo: "glob,glob"`, optional `excludeAgent: "code-review"\|"cloud-agent"`. Combined with the repo-wide file ([source](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)) |
| `AGENTS.md` | Anywhere, **nearest wins**. Alternative: a single root `CLAUDE.md`/`GEMINI.md` ([source](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)) |
| `.github/agents/NAME.agent.md` | `description` **required**. `tools` omitted/`["*"]` = all, `[]` = none, `server/tool`, `server/*`. `mcp-servers`/`metadata` cloud-only. `target: vscode\|github-copilot`. Prompt ≤ 30,000 chars. Repo > org > enterprise on name clash. Visible on GitHub.com once on the **default branch** ([source](https://docs.github.com/en/copilot/reference/custom-agents-configuration)) |
| `.github/skills/NAME/SKILL.md` | `name` (lowercase-hyphen) + `description` required. Loaded **when relevant**, can bundle scripts. Also `.claude/skills`, `.agents/skills`, personal `~/.copilot/skills` ([source](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)) |
| `.github/hooks/*.json` | `"version": 1`. Events such as `sessionStart`, `preToolUse` (can **deny**), `postToolUse`. Runs code. The cloud agent supports a subset ([source](https://docs.github.com/en/copilot/concepts/agents/hooks)) |

**Cloud agent loop guardrails** ([source](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)): write-access users only · one `copilot/` branch · draft PR, a human merges · the requester can't approve · workflows need **Approve and run** · firewall · hidden HTML comments filtered · 59-min Actions session · rulesets can block it unless you add a Copilot bypass ([about](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)).

**Azure DevOps MCP** ([remote](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server?view=azure-devops), [local](https://github.com/microsoft/azure-devops-mcp))
- **Remote (GA, recommended):** `https://mcp.dev.azure.com/{org}`, `type: http`, **Entra OAuth only**, **Entra-backed org** (no MSA). Headers `X-MCP-Toolsets: wit,work,repos,pipelines,wiki,testplan,advsec,elm` · `X-MCP-Tools` (not with toolsets) · `X-MCP-Readonly: true` · `X-MCP-Insiders`. Headers filter, they don't grant. Scopes `wit.read/write`, …; `Ado.Mcp.Tools` = legacy all-access.
- **Local:** `npx -y @azure-devops/mcp {org}` (`stdio`, Node 20+), `-d core work work-items …`, `-a interactive|azcli|env|envvar|pat`. Use it for Claude Desktop/Codex and the cloud agent.
- Free. Needs **agent mode**. Tools: `wit_work_item` (read), `wit_work_item_write` (`create`/`update`/`add_child`), `wit_work_item_comment_write`, `wit_work_item_link_write`.

**GitHub MCP** ([remote](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)): `https://api.githubcopilot.com/mcp/` (OAuth or PAT, VS Code 1.101+). Default toolsets `context,repos,issues,pull_requests,users`. `/readonly`, `/x/{one-toolset}[/readonly]`, `/x/all`, or headers `X-MCP-Toolsets`, `X-MCP-Tools`, `X-MCP-Readonly`, `X-MCP-Lockdown`. Remote-only: `create_pull_request_with_copilot`.

| | VS Code | Cloud agent / code review |
|---|---|---|
| Where | `.vscode/mcp.json` or user `mcp.json` | Repo **Settings → Copilot → MCP servers** (admin) |
| Shape | `{"servers":{}, "inputs":[]}`, `${input:id}` | `{"mcpServers":{}}`, **`tools` required** |
| Secrets | input prompts (`password: true`) | Agents secrets **`COPILOT_MCP_*`** → `$COPILOT_MCP_X` |
| Approval | you confirm tools | **none**: autonomous, tools only, **no OAuth remotes** |
| Built-ins | — | `github` (read-only, this repo) + `playwright` |

Sources: [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration), [repo MCP](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers). ADO in the cloud agent = local server + `azure/login` OIDC in `copilot-setup-steps.yml` (Actions sessions). The firewall doesn't apply directly to MCP servers ([source](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/customize-the-agent-firewall)). Learn MCP: `https://learn.microsoft.com/api/mcp`, no auth, free ([source](https://learn.microsoft.com/en-us/training/support/mcp)).

**Boards ↔ GitHub:** `AB#<id>` in an issue/PR description or commit links via the Boards app ([source](https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops)). **Create a pull request with GitHub Copilot** from a work item (GA): GitHub repos only, Boards connection via **GitHub App** (no PAT), cloud agent enabled, draft PR linked, status In Progress / Ready for Review / Error ([source](https://learn.microsoft.com/en-us/azure/devops/boards/github/work-item-integration-github-copilot?view=azure-devops)).

**ADO service hooks** ([create](https://learn.microsoft.com/en-us/azure/devops/service-hooks/create-subscription?view=azure-devops), [events](https://learn.microsoft.com/en-us/azure/devops/service-hooks/events?view=azure-devops), [webhooks](https://learn.microsoft.com/en-us/azure/devops/service-hooks/services/webhooks?view=azure-devops))
- `POST https://dev.azure.com/{org}/_apis/hooks/subscriptions?api-version=7.1`: `publisherId: tfs`, `eventType`, `resourceVersion: "1.0"`, `consumerId: webHooks`, `consumerActionId: httpRequest`, `publisherInputs.projectId` (GUID), `consumerInputs.url`. There's **no `az devops service-hooks`**, so use REST or the portal.
- Filters: `workitem.created` → `areaPath`, `workItemType`, `linksChanged`, `tag`. `build.complete` → `definitionName`, `buildStatus` (Succeeded/PartiallySucceeded/Failed/Stopped).
- **Project Admin** required. HTTPS only, no localhost. `basicAuthCredentials` / `httpHeaders` (visible to anyone who can view the subscription). Resource details **All / Minimal / None**. No payload signature. Free. History: `…/subscriptions/{id}/notifications`.

**PowerShell**
```powershell
# ~1 h Entra token for ADO REST (resource = Azure DevOps app ID), then POST the subscription JSON.
$token = (az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv).Trim()
# then: Invoke-RestMethod -Method Post -Uri "https://dev.azure.com/$org/_apis/hooks/subscriptions?api-version=7.1" -Headers @{Authorization="Bearer $token"} -ContentType application/json -Body $body
```

**Ubuntu (bash)**
```bash
# ~1 h Entra token for ADO REST (resource = Azure DevOps app ID), then POST the subscription JSON.
TOKEN=$(az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv)
# then: curl -s -X POST "https://dev.azure.com/$ORG/_apis/hooks/subscriptions?api-version=7.1" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$BODY"
```

**GitHub webhooks** ([REST](https://docs.github.com/en/rest/repos/webhooks), [validate](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)): `name: web`. `content_type` default **form**, so set `json`. `events` default `["push"]`. `secret` → `X-Hub-Signature-256: sha256=HMAC-SHA256(secret, raw body)`. Compare in **constant time**. SHA-1 `X-Hub-Signature` is legacy. Test vector: `It's a Secret to Everybody` + `Hello, World!` → `757107ea…3e17`. Ping `/pings`, `/deliveries`, redeliver `/attempts`. The `repo` scope includes hooks; `admin:repo_hook` is the narrow scope.

**Works in both**
```bash
# Create a JSON webhook with a secret; key[sub]=v builds nested JSON, key[]=v builds arrays; --jq .id prints the hook ID.
gh api repos/OWNER/REPO/hooks -X POST -f name=web -F active=true -f "events[]=issues" -f "config[url]=https://example.invalid/hook" -f "config[content_type]=json" -f "config[secret]=CHANGE_ME" --jq .id
```

**Cost:** MCP Server, service hooks, webhooks and Learn MCP are free. No Azure resources today. Agent mode uses your Copilot plan. The cloud agent uses premium requests plus the Actions/cloud allowance.
