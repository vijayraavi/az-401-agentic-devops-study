# Day 2 Cheat Sheet: Success metrics, Analytics/OData & docs-as-code (Domain 1, 15–20%)

**KPI → metric → widget/query → review.** A metric needs a definition, a data source, and a target. Velocity is for planning, not a KPI ([source](https://learn.microsoft.com/en-us/azure/devops/report/dashboards/team-velocity?view=azure-devops)). Don't make a metric the goal (Goodhart) ([DORA](https://dora.dev/guides/dora-metrics/)).

**DORA: five metrics** ([source](https://dora.dev/guides/dora-metrics/))
| Throughput | Instability |
|---|---|
| Change lead time (commit → prod) · Deployment frequency · Failed deployment recovery time (**replaced MTTR**) | Change fail rate · Deployment rework rate |
Speed and stability aren't a trade-off. Measure per app/service. Improve with smaller batches.

**Boards flow widgets** ([lead/cycle](https://learn.microsoft.com/en-us/azure/devops/report/dashboards/cycle-time-and-lead-time?view=azure-devops), [widgets](https://learn.microsoft.com/en-us/azure/devops/report/dashboards/analytics-widgets?view=azure-devops))
- **Lead time** = created → Completed. **Cycle time** = *first* In Progress → *final* Completed (reactivations included). DORA lead time ≠ Boards lead time.
- Scatter plot + moving average (N = 20% of days, odd) + std-dev band. Only **backlog** work item types. Team member to add to a team dashboard. Boards off = no widgets.
- **CFD** = items per column over time (bottlenecks/WIP). **Velocity** = credit to the sprint where the item is **completed**.

**Analytics OData** ([basics](https://learn.microsoft.com/en-us/azure/devops/report/extend-analytics/wit-analytics?view=azure-devops), [versions](https://learn.microsoft.com/en-us/azure/devops/report/extend-analytics/odata-api-version?view=azure-devops), [aggregation](https://learn.microsoft.com/en-us/azure/devops/report/extend-analytics/aggregated-data-analytics?view=azure-devops))
- `https://analytics.dev.azure.com/{org}/{project}/_odata/v3.0-preview/WorkItems?$filter=StateCategory eq 'Completed'&$select=WorkItemId,LeadTimeDays,CycleTimeDays`
- Versions: v1.0, **v2.0 (latest released)**, v3.0-preview, **v4.0-preview (latest preview)**. Leave out `/{project}` for cross-project.
- `$apply=filter(..)/groupby((WorkItemType), aggregate($count as N, CycleTimeDays with average as Avg))`; `compute(a div b as Pct)`
- Entity sets: `WorkItems`, `WorkItemBoardSnapshot` (CFD), `PipelineRuns` (Succeeded/FailedCount).
- Token (about 1 h) ([source](https://learn.microsoft.com/en-us/azure/devops/cli/entra-tokens?view=azure-devops)). In PowerShell, put OData URLs in single quotes (or escape `$` as `` `$ ``) so `$filter` / `$apply` / `$select` / `$count` are not treated as variables.

**PowerShell**
```powershell
# Short-lived (~1 h) Entra token for Azure DevOps. --resource 499b84ac-... is the ADO app ID, not ARM.
# --query accessToken -o tsv returns only the token; .Trim() strips a trailing newline.
$token = (az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv).Trim()
# Use it on Analytics OData calls. Keep $filter / $apply / $select in single quotes so PowerShell does not expand them.
# then: Invoke-RestMethod -Headers @{ Authorization = "Bearer $token" }
```

**Ubuntu (bash)**
```bash
# Short-lived (~1 h) Entra token for Azure DevOps. --resource 499b84ac-... is the ADO app ID, not ARM.
# --query accessToken -o tsv returns only the token string.
TOKEN=$(az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv)
# Use it on Analytics OData calls. Escape $filter / $apply / $select as \$ so bash does not expand them.
# then: curl -H "Authorization: Bearer $TOKEN"
```
- **Analytics views** = Boards data only, flat list, no pipelines, no Stakeholder access ([source](https://learn.microsoft.com/en-us/azure/devops/report/powerbi/what-are-analytics-views?view=azure-devops)). Power BI OData feed: `OmitValues = ODataOmitValues.Nulls, ODataVersion = 4` stops throttling ([source](https://learn.microsoft.com/en-us/azure/devops/report/powerbi/odataquery-connect?view=azure-devops)).
- **AI-assisted:** ADO remote MCP (`https://mcp.dev.azure.com/{org}`, GA, Entra, toolsets `wit,work,pipelines,wiki,repos,testplan,advsec,elm`, `X-MCP-Readonly`) in Copilot agent mode ([source](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server?view=azure-devops)). Check the OData it writes.

**Docs-as-code**
- **CODEOWNERS:** `.github/` → root → `docs/` (first found). Uses the **base branch** copy. **Last match wins**. Several owners on **one line**. Owners need **write**. No `!`/`[ ]`. Under 3 MB. Drafts don't auto-request. Any one owner's approval satisfies *Require review from Code Owners*. Protect `/.github/CODEOWNERS` ([source](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)). ADO equivalent (**works in both**) ([source](https://learn.microsoft.com/en-us/cli/azure/repos/policy/required-reviewer?view=azure-cli-latest)):

```bash
# Automatically include reviewers for matching paths (ADO's CODEOWNERS equivalent). --path-filter is a glob such as /docs/*.
az repos policy required-reviewer create --path-filter
```
- **Release notes:** `.github/release.yml` → `changelog.exclude.labels/authors`, `categories[].title` + `labels` (required), `"*"` catch-all ([source](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)). `gh release create v1.0.0 --generate-notes` (**works in both**; `--generate-notes` builds the body from merged PRs using `.github/release.yml`; `--notes` is prepended to that body).
- **LICENSE** in the root. No license = all rights reserved. The picker only appears at repo creation ([source](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)).
- **GitHub wiki:** public repos on Free. Private repos need Pro/Team/Enterprise ([source](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis)). Mermaid works in Markdown, issues, PRs and wikis ([source](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)).
- **ADO wiki:** provisioned (one per project, UI revert) vs **code wiki** (several wikis, versioned, `.order` file, PR edits) ([source](https://learn.microsoft.com/en-us/azure/devops/project/wiki/provisioned-vs-published-wiki?view=azure-devops)). `az devops wiki create --type codewiki --repository R --version main --mapped-path /docs` (**works in both**; `--type codewiki` publishes a repo folder as a versioned wiki, `--version` is the branch, `--mapped-path` is the folder). Mermaid: `::: mermaid` or a fence, and use **`graph`** not `flowchart` ([source](https://learn.microsoft.com/en-us/azure/devops/project/wiki/markdown-guidance?view=azure-devops)).
- **Copilot:** prompt files `.github/prompts/x.prompt.md` → `/x` (preview); `.github/copilot-instructions.md`; **cloud agent** (formerly coding agent): assign an issue → PR. It sees only comments made before assignment ([source](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github)).

**Cost:** Analytics, widgets, wiki and the MCP server are free. No Azure resources. Cloud agent uses premium requests plus Actions entitlement.
