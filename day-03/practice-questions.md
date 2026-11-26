# Day 3 Practice Questions (exam style)

### Q1
Your team uses GitHub Copilot in VS Code with an **Azure DevOps organization backed by Microsoft Entra ID**. Developers should be able to read and update work items from agent mode, with no local installation, and must **not** see pipeline, wiki, or repository tools. What should you add to `.vscode/mcp.json`?

- **A.** A `stdio` server running `npx -y @azure-devops/mcp <org>` with `"--authentication", "pat"`
- **B.** An `http` server with URL `https://mcp.dev.azure.com/<org>` and header `X-MCP-Toolsets: wit`
- **C.** An `http` server with URL `https://mcp.dev.azure.com/<org>` and header `X-MCP-Readonly: true`
- **D.** An `http` server with URL `https://api.githubcopilot.com/mcp/x/wit`

**Answer: B.** The remote Azure DevOps MCP Server (`https://mcp.dev.azure.com/{organization}`, streamable HTTP, Entra auth) needs no installation. `X-MCP-Toolsets: wit` limits the server to the work item tools. A is the local server, which needs Node.js and a PAT. C blocks updates and still exposes every toolset. D is the GitHub MCP server and has no `wit` toolset. [Source](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server?view=azure-devops)

### Q2
A repository admin wants the **Copilot cloud agent** to query the team's Azure DevOps work items while it works on assigned issues. The org is Entra-backed. Which configuration works?

- **A.** In repo **Settings → Copilot → MCP servers**, add `{"mcpServers":{"ado":{"type":"http","url":"https://mcp.dev.azure.com/<org>","tools":["*"]}}}` and sign in when prompted
- **B.** Commit `.vscode/mcp.json` with the remote Azure DevOps server. The cloud agent reads it automatically
- **C.** Add the local server (`npx -y @azure-devops/mcp <org> -a azcli`) with an explicit `tools` list in the repo MCP configuration, and add an OIDC `azure/login` step to `.github/workflows/copilot-setup-steps.yml` with `AZURE_CLIENT_ID`/`AZURE_TENANT_ID` as Agents secrets
- **D.** Store an Azure DevOps PAT in a repository Actions secret named `ADO_PAT` and reference it as `${{ secrets.ADO_PAT }}` in the MCP JSON

**Answer: C.** The cloud agent doesn't support remote MCP servers that use OAuth, so the Entra-only remote server (A) can't be used there. GitHub documents the local Azure DevOps server with `azcli` auth after an OIDC `azure/login` step in `copilot-setup-steps.yml` (Actions-based sessions). B is IDE-only config. D is wrong because the MCP configuration can only reference **Agents** secrets or variables whose names start with `COPILOT_MCP_`, not Actions secrets. [Source](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers)

### Q3
You're creating a custom agent for GitHub Copilot that reads Azure Boards and GitHub issues through MCP. It must **not** be able to edit files or run shell commands, even if a user asks it to. What should you put in `.github/agents/triage.agent.md`?

- **A.** A sentence in the prompt body: "Never edit files or run commands"
- **B.** `tools: ["read", "search", "ado/*", "github/*"]` in the YAML front matter
- **C.** `tools: ["*"]` plus an `AGENTS.md` that forbids edits
- **D.** Omit the `tools` property so the defaults apply

**Answer: B.** The `tools` property is an allow-list: only the listed aliases and MCP tools (`server/*`) are available, so `edit` and `execute` aren't. Omitting `tools` or using `["*"]` enables **all** tools (C, D). Prompt text and `AGENTS.md` guide the model but aren't a permission boundary (A, C). [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration), [VS Code custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)

### Q4
When a **build fails** in Azure DevOps project `Contoso`, an external incident service must receive a JSON payload over HTTPS. You must automate the setup from a script. What should you do?

- **A.** Run `az devops service-hooks create --event build.complete --url https://...`
- **B.** `POST https://dev.azure.com/{org}/_apis/hooks/subscriptions?api-version=7.1` with `publisherId: tfs`, `eventType: build.complete`, `publisherInputs: {projectId: <GUID>, buildStatus: Failed}`, `consumerId: webHooks`, `consumerActionId: httpRequest`, `consumerInputs: {url: https://...}`
- **C.** Create a team notification subscription for "A build fails" and set the delivery address to the service URL
- **D.** `POST https://api.github.com/repos/{owner}/{repo}/hooks` with `events: ["workflow_run"]`

**Answer: B.** Service hook subscriptions are created with the Subscriptions REST API, using the `tfs` publisher, the `build.complete` event with a `buildStatus` filter, and the Web Hooks consumer (`webHooks`/`httpRequest`). There's no `az devops service-hooks` command group (A). Notifications send email, not JSON to an endpoint (C). D is a GitHub webhook. [Create a subscription](https://learn.microsoft.com/en-us/azure/devops/service-hooks/create-subscription?view=azure-devops), [events](https://learn.microsoft.com/en-us/azure/devops/service-hooks/events?view=azure-devops)

### Q5
A receiver for a GitHub repository webhook must reject forged or tampered requests. The webhook was created with `config.secret` set. What should the receiver do?

- **A.** Compare the `X-GitHub-Delivery` header with a list of known GUIDs
- **B.** Parse the JSON, re-serialize it, compute SHA-256 of the result and compare with `==` to `X-Hub-Signature`
- **C.** Compute HMAC-SHA256 of the **raw** request body with the secret, prefix `sha256=`, and compare it to `X-Hub-Signature-256` with a constant-time comparison
- **D.** Check that the request came from `api.github.com` by reverse DNS

**Answer: C.** GitHub signs each delivery with an HMAC-SHA256 hex digest of the payload, keyed with your secret, and sends it as `X-Hub-Signature-256: sha256=...`. Verify it over the unmodified body with a constant-time compare, never a plain `==`. `X-Hub-Signature` (SHA-1) is legacy, and re-serializing changes the bytes (B). [Validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)
