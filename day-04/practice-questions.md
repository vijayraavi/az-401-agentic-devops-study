# Day 4 Practice Questions (exam style)

### Q1
Your team ships a product that customers run in three supported versions. A critical bug is found. You must fix it for all supported versions while keeping `main` as the single integration branch, and you want exact control over which commits are ported. Which approach should you use?

- **A.** Use Git flow: merge the release branch into `main`, then merge `main` into every other release branch
- **B.** Tag each release and delete the release branches, then merge the fix into the tags
- **C.** Make the fix on `main` through a pull request, then cherry-pick it into each `release/*` branch through its own pull request
- **D.** Merge `main` into each release branch so that all changes since the last release come along

**Answer: C.** Microsoft's branching guidance uses long-lived release branches that aren't merged back to `main`. Fixes land in the mainline and are **cherry-picked** (not merged) into the release branches, because merging can drag unwanted release-specific or unrelated changes across. A creates the double-merge pattern of Git flow, which isn't trunk-based. B is wrong because tags aren't branches: Microsoft advises release branches, since tags are pushed separately and easy to forget. D merges everything, which defeats exact control. [Source](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance?view=azure-devops)

### Q2
In Azure Repos, you need every current and future branch under `release/` (for example `release/20` and `release/21`) to require two approvals before a PR can be completed. You use `az repos policy`. What should you do?

- **A.** Create an approver-count policy for each release branch with `--branch-match-type exact`
- **B.** Create one approver-count policy with `--branch release/ --branch-match-type prefix --minimum-approver-count 2`
- **C.** Create one approver-count policy with `--branch main` and rely on it being inherited by `release/*`
- **D.** Create a required-reviewer policy with a path filter of `release/*`

**Answer: B.** Azure Repos policies can apply to one branch (`exact`) or to a branch folder such as `release/` with `prefix`, so a single policy also covers future branches. A works for today's branches only. C is wrong because policies are evaluated against the **target** branch of the PR and don't inherit from `main`. D is wrong because path filters match **file paths** inside a PR, not branch names (and a path that doesn't start with `/` or a wildcard has no effect). [Source](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies?view=azure-devops)

### Q3
A repository on GitHub requires one approving review on `main` through a ruleset. A developer assigns an issue to the Copilot cloud agent. The agent opens a draft PR from a `copilot/` branch. The developer reviews the code and approves it, but the PR can't be merged and the required `build` check shows as pending. What should you do? (Choose the best answer.)

- **A.** Disable the ruleset's pull request rule, because agents can't satisfy it
- **B.** Ask Copilot to mark the PR ready for review and approve it
- **C.** Add the Copilot app to the bypass list so its PR merges automatically
- **D.** Have a user with write access click **Approve and run workflows** so the check runs, and have a different person approve the PR

**Answer: D.** By default Actions workflows don't run on cloud-agent pushes until a user with write access clicks **Approve and run workflows**, so required checks stay pending. The person who asked Copilot for the PR can't approve it, so another reviewer must (and if the PR is opened under Copilot's own app identity, one more approval than configured is needed). A removes the control you want. B is impossible because Copilot cannot mark its PR ready, approve, or merge. C is wrong because the agent can't merge, and a bypass would defeat review. [Source](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)

### Q4
You enabled Copilot code review for your Azure DevOps organization and added the **Automatically request Copilot code review** branch policy to `main`. Your team wants to treat Copilot's review as one of the two required approvals. What will happen?

- **A.** It can't count: Copilot always leaves a Comment review, so it doesn't satisfy reviewer policies or block merging, and humans must still approve
- **B.** It counts automatically once Copilot reports "no issues"
- **C.** It counts if you add *GitHub Copilot* as a required reviewer
- **D.** It blocks merging until you resolve every Copilot comment, even without a comment-resolution policy

**Answer: A.** In Azure Repos, Copilot "always leaves a Comment review. It never approves the pull request or requests changes, so its review doesn't satisfy required-reviewer policies and doesn't block merging." The GA announcement says the same: Copilot doesn't approve pull requests or block merges. You still need human approvals through *Require a minimum number of reviewers*. [Source](https://learn.microsoft.com/en-us/azure/devops/repos/git/copilot-code-reviews?view=azure-devops)

### Q5
You're the only admin of a GitHub repository. A ruleset on the default branch requires pull requests. For emergencies, you want admins to be able to merge a PR that doesn't meet the review requirements, but you want to make sure nobody, including admins, can push commits directly to the branch. How should you configure the ruleset?

- **A.** Add the Admin repository role to `bypass_actors` with `bypass_mode: always`
- **B.** Don't add bypass actors, and temporarily set `enforcement` to `disabled` during an emergency
- **C.** Add the Admin repository role to `bypass_actors` with `bypass_mode: pull_request`
- **D.** Add the Admin repository role with `bypass_mode: exempt`

**Answer: C.** `pull_request` mode means the actor can bypass the rules only on pull requests, so an admin can use **Merge without waiting for requirements** but direct pushes are still blocked, and bypasses are logged. `always` (A) also allows direct pushes. `exempt` (D) skips the rules entirely and doesn't even create an audit entry. B works but weakens the protection for everyone while disabled. [Source](https://docs.github.com/en/rest/repos/rules)
