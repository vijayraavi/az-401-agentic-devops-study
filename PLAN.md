# AZ-401 19-Day Study Plan (Tue 24 Nov → Sat 12 Dec 2026, IST)

**Exam:** AZ-401 *Designing and Implementing Microsoft Agentic DevOps Solutions* (beta), **Sunday 13 Dec 2026, 1:30 PM IST**.
**Source of domains/weights:** official study guide: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-401 (fetched 24 Nov 2026).

## How the days are weighted
16 learning days + 3 revision/mock days. Learning days are split by the midpoint of each domain's weight:

| Domain | Official weight | Midpoint | Learning days | Share of 16 |
|---|---|---|---|---|
| Processes & communications | 15–20% | 17.5% | 3 (D1–D3) | 19% |
| Source control strategy | 10–15% | 12.5% | 2 (D4–D5) | 12.5% |
| Build & release pipelines | 35–40% | 37.5% | 6 (D6–D11) | 37.5% |
| Security & compliance | 15–20% | 17.5% | 3 (D12–D14) | 19% |
| Instrumentation | 15–20% | 17.5% | 2 (D15–D16) + ½ of D17 | ~15% |

Daily rhythm (~2–3 h): 30 min concepts → 60–90 min hands-on lab (Azure DevOps **and** GitHub) → 20 min cheat sheet → 15 min 5 practice questions → cleanup.
Rules: YAML pipelines only (no classic release), workload identity federation / OIDC (no stored client secrets), Copilot cloud/coding agent + MCP, GitHub Agentic Workflows, Microsoft Foundry where relevant. Keep Azure spend near zero and clean up every lab.

## Day-by-day

| Day | Date (IST) | Domain | Topic | Key hands-on |
|---|---|---|---|---|
| 01 | Tue 24 Nov | Processes | Orientation + flow of work & traceability (plan→build→deploy→operate, Azure Boards, Boards↔GitHub `AB#` links, notifications) | ADO project + work items via `az boards`, work-item-linking branch policy, GitHub repo with Boards app + Actions traceability gate |
| 02 | Wed 25 Nov | Processes | Success metrics (DORA, cycle/lead time, KPIs→metrics), Analytics/OData & AI-assisted queries; documenting with Copilot (wiki, README, CHANGELOG, LICENSE, CODEOWNERS, releases, Mermaid diagrams) | Cycle-time widgets, Analytics query, Copilot-generated CHANGELOG + CODEOWNERS |
| 03 | Thu 26 Nov | Processes | Agentic collaboration: requirements for agents/skills/loops (custom instructions, AGENTS.md, custom agents), Azure DevOps remote MCP server, GitHub MCP server, webhooks/service hooks, Boards↔GitHub via MCP | `mcp.json` with ADO + GitHub MCP, service hook → webhook |
| 04 | Fri 27 Nov | Source control | Branching strategies (trunk, feature, release, Git worktree, Git flow, GitHub flow); PR workflows; ADO branch policies vs GitHub rulesets/branch protection; rules for Copilot agent PRs | Branch policies (`az repos policy`), GitHub ruleset, Copilot-authored PR review flow |
| 05 | Sat 28 Nov | Source control | Repo permissions, tags, traceability (coverage, quality, deep links), Git hooks, ADO→GitHub migration (GitHub Enterprise Importer), recovering/removing data (reflog, revert, `git filter-repo`) | pre-commit hook, `gh ado2gh` dry run, purge a secret from history |
| 06 | Sun 29 Nov | Pipelines | Package management: Azure Artifacts feeds, views, upstream sources vs GitHub Packages; SemVer vs CalVer; pipeline artifact versioning | Feed + `@Release` view, publish npm package from YAML & Actions |
| 07 | Mon 30 Nov | Pipelines | Testing strategy & quality/release gates (unit, integration, load); test tasks, test results, code coverage with Copilot + MCP | PublishTestResults/coverage in YAML; Actions test report; Copilot-generated tests |
| 08 | Tue 1 Dec | Pipelines | Azure Pipelines vs GitHub Actions; agent/runner infra (Microsoft-hosted, self-hosted, Managed DevOps Pools, larger runners, cost/licences); Azure Pipelines ↔ GitHub repos; trigger rules | Pipeline on a GitHub repo, path/branch filters, scheduled triggers |
| 09 | Wed 2 Dec | Pipelines | Multi-stage YAML, `dependsOn`/conditions, matrix/parallelism, templates, variables & variable groups, environments with checks/approvals; YAML via Copilot; **GitHub Agentic Workflows** (`gh aw`) | Template-based 3-stage pipeline with environment approval; first agentic workflow |
| 10 | Thu 3 Dec | Pipelines | Deployment strategies (blue-green, canary, ring, progressive exposure, feature flags, A/B), dependency ordering, slots/swap, rolling, hotfix path, resiliency; containers/binaries/scripts/DB tasks | App Service F1/B1 slot swap (cleanup same day), container deploy via OIDC |
| 11 | Fri 4 Dec | Pipelines | IaC & config management (Bicep, what-if, deployment stacks); maintaining pipelines (failure rate, duration, flaky tests, cost/time optimisation, retention) | Bicep deploy from YAML + Actions, retention policy settings, pipeline analytics |
| 12 | Sat 5 Dec | Security | AuthN/AuthZ: service principal vs managed identity, **workload identity federation** service connections, GitHub OIDC, GitHub Apps vs `GITHUB_TOKEN` vs PATs, ADO permissions/access levels/teams | WIF service connection + Actions `azure/login` with OIDC |
| 13 | Sun 6 Dec | Security | Sensitive info: Key Vault in Pipelines & Actions, secrets/keys/certs, secure files, GitHub secrets/environments, leakage prevention | Key Vault (RBAC) → variable group & Actions, log masking demo |
| 14 | Mon 7 Dec | Security | Scanning: GitHub Advanced Security & GHAS for Azure DevOps (dependency, code, secret scanning, push protection), Defender for Cloud DevOps security connectors | Enable CodeQL/secret scanning on lab repo, Defender DevOps connector (free foundational CSPM) |
| 15 | Tue 8 Dec | Instrumentation | Dashboards (flow, cycle time, MTTR, lead time), Azure Monitor/Log Analytics integration with ADO & GitHub, GitHub Insights charts, alerts for pipelines/Actions | Log Analytics workspace (small, cleanup), Projects insights chart, pipeline failure alert |
| 16 | Wed 9 Dec | Instrumentation | AI agents for ops: Azure SRE Agent, Azure Copilot observability agent; App Insights distributed tracing; CPU/mem/disk/network analysis; Copilot agent logs; KQL & natural-language queries | KQL drills, SRE Agent walkthrough (docs/demo), Copilot session logs |
| 17 | Thu 10 Dec | Revision | Weak-area review + pipelines (35–40%) re-drill + instrumentation KQL top-up | Re-run hardest labs from notes |
| 18 | Fri 11 Dec | Mock | Two timed mock exams (case-study style), review every miss against the study guide bullet | Mock 1 & 2 + error log |
| 19 | Sat 12 Dec | Revision | Light review of all cheat sheets, exam logistics (ID, Pearson VUE check-in), early night | Final 30-question rapid fire |

Exam: **Sun 13 Dec 2026, 1:30 PM IST**. Passing score 700 (beta results are not immediate) — https://learn.microsoft.com/en-us/credentials/certifications/exams/az-401/
