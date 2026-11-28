# Day 5 Practice Questions (exam style)

### Q1
Your company is migrating 40 Azure DevOps Services repositories to a GitHub Enterprise Cloud organization with GitHub Enterprise Importer (`gh ado2gh`). A security architect wants the migration to authenticate to GitHub without long-lived secrets. What should you tell them?

- **A.** Use a fine-grained personal access token scoped to the destination organization.
- **B.** Use a GitHub App installation token for the destination organization.
- **C.** GEI requires a personal access token (classic). An organization owner needs the `repo`, `workflow` and `admin:org` scopes. Create it with a short expiry and revoke it after the migration.
- **D.** Use OpenID Connect workload identity federation from Microsoft Entra ID.

**Answer: C.** GEI supports only personal access tokens (classic) for GitHub. Fine-grained PATs, GitHub Apps and OIDC aren't supported. Owners need `repo`, `workflow` and `admin:org`, and migrators need `repo`, `workflow` and `read:org`. The Azure DevOps side also uses a PAT. [Source](https://docs.github.com/en/migrations/using-github-enterprise-importer/ado/manage-access)

### Q2
A developer pushed a commit containing a production database password to a GitHub repository three days ago. Several teammates have pulled since. What should you do **first**?

- **A.** Run `git revert` on the commit and push.
- **B.** Rotate (revoke and replace) the password.
- **C.** Run `git filter-repo --sensitive-data-removal` in a fresh clone and force-push.
- **D.** Delete the repository and re-create it from a clean copy.

**Answer: B.** Rewriting history doesn't remove copies already in clones, forks, PR refs or caches, so the secret must be treated as compromised and rotated first. `git revert` leaves the secret in history. Rewriting with `git filter-repo` and coordinating with GitHub Support comes after rotation. [Source](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

### Q3
A repository on GitHub.com used **tag protection rules** to stop contributors from deleting `v*` release tags. You need equivalent protection today with the least administrative effort. What should you configure?

- **A.** Re-create the tag protection rules under **Settings → Tags**.
- **B.** A repository ruleset that targets tags matching `v*`, with **Restrict deletions** (and **Restrict updates**) enabled.
- **C.** A classic branch protection rule with the pattern `v*`.
- **D.** A `CODEOWNERS` entry for `refs/tags/v*`.

**Answer: B.** GitHub sunset tag protection rules in 2024 and converted them to rulesets. Tag rulesets (`target: tag`) can restrict creation, updates, deletions and force pushes. Branch protection rules and CODEOWNERS don't apply to tags. [Source](https://github.blog/changelog/2024-05-29-sunset-notice-tag-protections/) · [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)

### Q4
Your team shares a `pre-commit` hook through `git config core.hooksPath .githooks` that blocks files containing credentials. A developer bypassed it with `git commit --no-verify` and pushed a GitHub personal access token to your **public** GitHub repository. You need a control that the developer can't bypass locally. What should you implement?

- **A.** A `commit-msg` hook that rejects commits without a work item reference.
- **B.** A `pre-push` hook distributed through `core.hooksPath`.
- **C.** Secret scanning with **push protection** enabled on the repository.
- **D.** A global `core.hooksPath` set on every developer workstation.

**Answer: C.** Client-side hooks run on the developer's machine. They aren't cloned automatically, and `--no-verify` skips them (the `pre-push` hook can be skipped too). Push protection runs on GitHub's server during the push and blocks supported secrets. Only a user with bypass rights can allow the push, and the bypass is audited. It's free for public repositories. [Source](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection) · [githooks](https://git-scm.com/docs/githooks)

### Q5
In Azure Repos, a developer deleted the `release/2.3` branch six weeks ago. The branch had a minimum-reviewers policy and a branch-level Deny permission. You need the branch back with its commits. What's true?

- **A.** It can't be restored, because deleted branches are kept for only 30 days.
- **B.** Search for the exact branch name on the **Branches** page, then select **Restore branch**. Reapply the branch policies and permissions afterwards.
- **C.** Restore it from the repository recycle bin under **Project settings → Repositories**, which also restores its policies.
- **D.** Run `git reflog` on the Azure DevOps server to find the commit.

**Answer: B.** Azure Repos keeps deleted branches with no time limit. You restore one by searching for its full name on the Branches page (or by recreating the ref at the last commit). Restoring doesn't bring back branch policies or permissions. The recycle bin is for deleted **repositories** (30 days), not branches. [Source](https://learn.microsoft.com/en-us/azure/devops/repos/git/restore-deleted-branch?view=azure-devops)
