# Day 2 Practice Questions (exam style)

### Q1
Leadership wants one number that shows how long customers wait from the moment they **report** a bug until the fix is **done**. Your team tracks bugs in Azure Boards. Which widget and configuration should you use?

A. Cycle Time widget, work items = Bug
B. Lead Time widget, work items = Bug
C. Velocity widget, by count of Bugs
D. Cumulative Flow Diagram on the Bugs backlog

**Answer: B.** Lead time runs from when the work item is **created** to when it reaches a Completed state, which is the customer's wait. Cycle time starts only when work first moves **In Progress**, so it leaves out queue time. Velocity and CFD don't measure elapsed time per item. [Source](https://learn.microsoft.com/en-us/azure/devops/report/dashboards/cycle-time-and-lead-time?view=azure-devops)

### Q2
You're defining DevOps success metrics using DORA's current model. A stakeholder asks which metric replaced *mean time to restore (MTTR)*, and which two metrics measure **instability**. What do you answer?

A. Replaced by change lead time. Instability = deployment frequency and change fail rate
B. Replaced by failed deployment recovery time. Instability = change fail rate and deployment rework rate
C. Replaced by cycle time. Instability = change fail rate and MTTR
D. MTTR wasn't replaced. Instability = change fail rate only

**Answer: B.** DORA's five-metric model groups change lead time, deployment frequency, and **failed deployment recovery time** (which replaced MTTR) as throughput. **Change fail rate** and **deployment rework rate** measure instability. [Source](https://dora.dev/guides/dora-metrics/)

### Q3
You need a Power BI report of **pipeline run pass/fail counts** and **average cycle time per work item type**, aggregated on the server to keep refreshes small. A colleague suggests the *Azure DevOps (Boards only)* connector with an Analytics view. What should you do?

A. Use the Analytics view. It supports pipelines and work items
B. Use OData feed queries against `PipelineRuns` and `WorkItems` with `$apply` aggregation, and set `OmitValues = ODataOmitValues.Nulls`
C. Export WIQL query results to CSV each day
D. Use an Analytics view with the "All history by month" option

**Answer: B.** Analytics views only support Boards (work item) data, as a flat list with no pipelines. OData queries can aggregate on the server with `$apply`, and `ODataOmitValues.Nulls` stops Power Query from making a request per null value, which leads to throttling. [Analytics views](https://learn.microsoft.com/en-us/azure/devops/report/powerbi/what-are-analytics-views?view=azure-devops), [OData + Power BI](https://learn.microsoft.com/en-us/azure/devops/report/powerbi/odataquery-connect?view=azure-devops), [PipelineRuns sample](https://learn.microsoft.com/en-us/azure/devops/report/powerbi/sample-pipelines-outcome-summary?view=azure-devops)

### Q4
A repository has `CODEOWNERS` files in both `docs/` and `.github/`. The `.github/CODEOWNERS` file contains:
```text
*.md      @org/docs-team
/api/     @org/api-team
*         @org/platform
```
A PR into `main` changes only `/api/README.md`. Who is automatically requested for review?

A. @org/docs-team only
B. @org/api-team only
C. @org/platform only
D. All three teams

**Answer: C.** GitHub uses the first file it finds in the order `.github/` → root → `docs/`, so `.github/CODEOWNERS` applies. Inside that file the **last matching pattern wins**. `*` is last and matches every file, so only @org/platform is requested. To get the specific owners, put `*` **first**. [Source](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

### Q5
You want GitHub release notes to group merged PRs into "Features" and "Fixes" by label, leave out Dependabot PRs (they carry the `dependencies` label), and put everything else under "Other". Releases are created from a workflow with the GitHub CLI. What should you implement?

A. A `CHANGELOG.md` maintained by hand, plus `gh release create --notes-file CHANGELOG.md`
B. `.github/release.yml` with `changelog.exclude.labels: [dependencies]` and categories by label including a `"*"` catch-all, plus `gh release create <tag> --generate-notes`
C. `.github/release.yml` with a `labels` list only, plus `gh release create --notes-from-tag`
D. A CODEOWNERS entry for Dependabot

**Answer: B.** Automatically generated release notes read `.github/release.yml`. `changelog.exclude.labels` (or `exclude.authors`) removes PRs from the notes, each category needs `title` + `labels`, and `"*"` catches everything that didn't match. `gh release create --generate-notes` uses the Release Notes API. [Release notes config](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes), [gh release create](https://cli.github.com/manual/gh_release_create)
