# Day 1 Cheat Sheet: Flow of work & traceability (Domain 1, 15–20%)

**Flow:** PLAN (Boards/Issues) → BUILD (Repos, PRs, CI) → DEPLOY (YAML stages / Actions + environments) → OPERATE (Monitor, App Insights, SRE Agent) → FEEDBACK (notifications, service hooks, new work items) → PLAN

**Processes** ([source](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/choose-process?view=azure-devops))
| Basic | Agile | Scrum | CMMI |
|---|---|---|---|
| Epic/Issue/Task | Epic/Feature/**User Story**/Bug/Task | Epic/Feature/**PBI**/Bug/Task | Epic/Feature/**Requirement**/Change Request |

**AB# rules** ([source](https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops))
- Links from a commit message, PR **description**, or issue **description**. A PR **title** or comment does **not** link.
- `Fixes AB#1` moves the item to the first Resolved-category state (Completed if there's none). `Closed AB#1` moves it to the Closed state.
- Transitions happen **only on merge to the default branch**.
- 1 GitHub repo connects to 1 ADO org. If links fail, check the Azure Boards identity's area-path permissions ([source](https://learn.microsoft.com/en-us/azure/devops/boards/github/connect-to-github?view=azure-devops)).

**Enforce traceability**
- ADO: branch policy *Check for linked work items* (**works in both** PowerShell and bash) ([source](https://learn.microsoft.com/en-us/cli/azure/repos/policy/work-item-linking?view=azure-cli-latest)):

```bash
# Require a linked work item on PRs into main. --repository-id is the repo GUID (`az repos show --query id`).
# --blocking true fails the PR if none is linked; --enabled true turns the policy on.
az repos policy work-item-linking create --repository-id <id> --branch main --blocking true --enabled true
```
- GitHub: **ruleset** with required PR + required status check (an Actions job that greps the PR body for `AB#\d+`) ([source](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets))
- In Actions, pass `github.event.pull_request.body` through `env:`, never inline `${{ }}` in `run:`, to avoid script injection. Set `permissions: contents: read`.

**Feedback channels**
- Notifications: personal / team / project subscriptions ([source](https://learn.microsoft.com/en-us/azure/devops/organizations/notifications/about-notifications?view=azure-devops))
- Service hooks: push ADO events to Teams, Slack, Web Hooks, and others ([source](https://learn.microsoft.com/en-us/azure/devops/service-hooks/overview?view=azure-devops))
- Lead time = created → done. Cycle time = started (In Progress) → done ([source](https://learn.microsoft.com/en-us/azure/devops/report/dashboards/cycle-time-and-lead-time?view=azure-devops))

**MCP (agentic traceability)**
| | Azure DevOps remote MCP | GitHub remote MCP |
|---|---|---|
| URL | `https://mcp.dev.azure.com/{org}` | `https://api.githubcopilot.com/mcp/` |
| Auth | Microsoft Entra ID (org must be **Entra-backed**, not MSA) | OAuth or PAT |
| Scope | `X-MCP-Toolsets: wit,repos,...`, `X-MCP-Readonly` | `X-MCP-Toolsets`, `/readonly` or `X-MCP-Readonly` |
| Source | [docs](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server?view=azure-devops) | [docs](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md) |
Local ADO MCP server = Node 20+ via `npx`, stdio transport, PAT or Entra. Use it only when your client can't do Entra auth to the remote server.

**Costs:** ADO first 5 Basic users + 1 hosted parallel job (1,800 min/mo) are free ([source](https://learn.microsoft.com/en-us/azure/devops/organizations/billing/billing-faq?view=azure-devops)). The ADO MCP server itself is free ([source](https://learn.microsoft.com/en-us/azure/devops/mcp-server/mcp-server-overview?view=azure-devops)).
