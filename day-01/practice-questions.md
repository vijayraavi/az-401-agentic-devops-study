# Day 1 Practice Questions (exam style)

### Q1
Your team uses Azure Boards with GitHub repositories connected through the Azure Boards app. A developer opens a PR titled `Fix login AB#412` with an empty description. The PR is merged into `main` (the default branch). What happens to work item 412?

- **A.** It's linked and moved to Resolved
- **B.** It's linked but its state doesn't change
- **C.** It isn't linked and its state doesn't change
- **D.** It's linked and moved to Closed

**Answer: C.** `AB#` in a PR **title** doesn't create a link. Only commit messages, PR descriptions, and issue descriptions do. With no link, no transition happens either. [Source](https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops)

### Q2
A PR description contains `Fixes AB#88`. The PR targets `release/2.1` (not the default branch) and is merged. The project uses the Agile process. What's the result?

- **A.** Work item 88 is linked and moved to Resolved
- **B.** Work item 88 is linked; its state isn't changed
- **C.** Work item 88 is moved to Closed
- **D.** The merge is blocked

**Answer: B.** The link is created, but state-transition rules apply only when the PR merges into the **default branch**. [Source](https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops)

### Q3
You must ensure every pull request into `main` in an **Azure Repos** repository references at least one Azure Boards work item, and PRs without one can't be completed. What should you configure?

- **A.** A service hook on *Pull request created*
- **B.** A branch policy *Check for linked work items* set to **Required**
- **C.** A team notification subscription
- **D.** A build validation policy that runs a YAML pipeline

**Answer: B.** The *Check for linked work items* branch policy, set to Required (`--blocking true`), blocks completion. D could be made to work but adds pipeline cost and maintenance. The built-in policy is the intended answer. [Branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies?view=azure-devops), [CLI](https://learn.microsoft.com/en-us/cli/azure/repos/policy/work-item-linking?view=azure-cli-latest)

### Q4
You want GitHub Copilot in VS Code agent mode to read Azure Boards work items and pull requests without being able to modify anything, and without installing a local server. Your Azure DevOps organization is backed by Microsoft Entra ID. Which `mcp.json` setting meets the requirement?

- **A.** `"url": "https://mcp.dev.azure.com/<org>"` with header `X-MCP-Readonly: true` and `X-MCP-Toolsets: wit,repos`
- **B.** A local server via `npx` with a full-scope PAT
- **C.** `"url": "https://api.githubcopilot.com/mcp/"` only
- **D.** `"url": "https://mcp.dev.azure.com/<org>"` with toolset `all`

**Answer: A.** The remote Azure DevOps MCP Server needs no install. It authenticates with Entra ID, and the `X-MCP-Toolsets` and `X-MCP-Readonly` headers restrict it to read-only work-item and repo tools, which is least privilege. B needs a local install and an over-scoped PAT. C is the GitHub server. D allows writes. [Source](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server?view=azure-devops)

### Q5
A GitHub repository is connected to an Azure Boards project in the **Contoso** organization. Another team wants to connect the same repository to their project in the **Fabrikam** organization so `AB#` mentions link to their work items too. What should you recommend?

- **A.** Connect the repo to both organizations. `AB#` resolves by project name
- **B.** Keep the repo connected to only one organization, because work item IDs aren't unique across organizations and the Boards app prevents multi-org connections
- **C.** Use `AB#Fabrikam/123` syntax
- **D.** Use a PAT-based connection for the second organization

**Answer: B.** Connect a GitHub repo to projects in a **single** Azure DevOps organization. IDs can collide across orgs, and the Azure Boards app prevents connecting to multiple organizations. [Source](https://learn.microsoft.com/en-us/azure/devops/boards/github/connect-to-github?view=azure-devops)
