# Day 4 Cheat Sheet: Branching strategies, PR workflows, policies vs rulesets, Copilot agent PRs (Domain 2, 10–15%)

**Strategies** ([guidance](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance?view=azure-devops), [Release Flow](https://learn.microsoft.com/en-us/devops/develop/how-microsoft-develops-devops))

| Strategy | One-liner | Use when |
|---|---|---|
| Feature branch | Topic branch per change → PR → protected `main`. Name: `users/<n>/<topic>`, `feature/…`, `bugfix/…`, `hotfix/…` | Default. Long work → **feature flags** |
| Trunk-based | Short-lived branches, one buildable trunk. Microsoft **Release Flow** = trunk + release branches | Many devs, strong CI |
| Release branch | `release/NN` from `main`, long-lived, **not** merged back by PR. Fix on `main` → **cherry-pick** (new branch + PR) | Several supported versions |
| Git worktree | `git worktree add [-b new] <path> [branch]` · `list` · `remove` · `prune`. One branch per worktree | Parallel reviews, hotfixes, agent tasks ([docs](https://git-scm.com/docs/git-worktree)) |
| Git flow | `main` + `develop` + `feature/release/hotfix`; releases/hotfixes merged twice | Versioned software; not for CD ([nvie](https://nvie.com/posts/a-successful-git-branching-model/)) |
| GitHub flow | branch → commit → PR → review → merge → delete branch; `main` deployable | Continuous delivery ([doc](https://docs.github.com/en/get-started/using-github/github-flow)) |

Tags vs release branches: Microsoft prefers branches; tags are pushed separately and easy to forget. Two reviewers is "optimal based on research".

**Azure Repos branch policies** ([doc](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies?view=azure-devops), [CLI](https://learn.microsoft.com/en-us/cli/azure/repos/policy?view=azure-cli-latest))

| Policy | CLI (`az repos policy …`) | Notes |
|---|---|---|
| Min reviewers | `approver-count create --minimum-approver-count N --creator-vote-counts --reset-on-source-push --allow-downvotes` | "Prohibit most recent pusher" = portal / `--config` |
| Linked work items | `work-item-linking create` | Required vs Optional (`--blocking`) |
| Comment resolution | `comment-required create` | |
| Merge types | `merge-strategy create --allow-squash/--allow-rebase/--allow-rebase-merge/--allow-no-fast-forward` | Squash = linear history |
| Build validation | `build create --build-definition-id --valid-duration --manual-queue-only` | Pipeline must exist first |
| Required reviewers | `required-reviewer create --required-reviewer-ids --message --path-filter` | Path must start with `/` or wildcard |
| Scope | `--branch main` (exact) · `--branch release/ --branch-match-type prefix` | Evaluated on the **target** branch |
| Other | `list`, `show`, `update`, `delete --id`, `create --config file` | Need Project Admin or **Edit policies** |
| Bypass | permissions: *when completing PRs*, *when pushing* | Can't delete a branch with required policies |

**GitHub rulesets vs classic protection** ([rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [REST](https://docs.github.com/en/rest/repos/rules))

| | Rulesets | Classic branch protection |
|---|---|---|
| Stacking | Many apply; **most restrictive wins** | **One** rule per branch |
| Status | `active` / `disabled` (`evaluate` = Enterprise only) | Delete to turn off |
| Bypass | `bypass_actors`: role (Admin = **5**), team, app, user · mode `always` / `pull_request` / `exempt` | Admins bypass unless enforce-admins |
| Visibility | Anyone with read access | Admins |
| Patterns | `fnmatch`, `~DEFAULT_BRANCH`, `~ALL`, `refs/heads/release/**` | fnmatch |

REST: `POST /repos/{o}/{r}/rulesets` (`gh api --method POST … --input file.json`) · `GET …/rules/branches/{branch}` · `gh ruleset list|view|check`. Rule types: `pull_request` (`required_approving_review_count` 0–10, `dismiss_stale_reviews_on_push`, `require_last_push_approval`, `require_code_owner_review`, `required_review_thread_resolution`, `allowed_merge_methods`, `require_extra_approval_for_unattributed_changes`), `required_status_checks` (strict/loose), `required_linear_history`, `merge_queue` (workflows need `merge_group`), `creation/update/deletion/non_fast_forward`, `required_signatures`, `copilot_code_review` (`review_on_push`, `review_draft_pull_requests`), `code_scanning`.

**Copilot cloud agent PR rules** ([risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations), [review output](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output))

| Rule | Detail |
|---|---|
| Who | Only users with **write** access can trigger it |
| Branch | Only one: new `copilot/…` branch, or the PR branch when you `@copilot` there. Subject to protections and required checks |
| PR | **Draft**. Agent can't mark ready, approve or merge. Commits signed, you are co-author |
| Workflows | Don't run until a writer clicks **Approve and run workflows**. Admin can turn off *Require approval for workflow runs* (Settings → Copilot → cloud agent), risky |
| Approvals | Requester **can't** approve. PR under Copilot's own identity needs **+1** approval (ruleset setting, public preview, on by default; always for classic) |
| Validation | CodeQL, advisory check, secret scanning, Copilot code review (no GHAS licence needed) |

**Copilot code review is advisory by default** ([GitHub](https://docs.github.com/en/copilot/concepts/agents/code-review), [Azure Repos](https://learn.microsoft.com/en-us/azure/devops/repos/git/copilot-code-reviews?view=azure-devops))
- GitHub: ruleset rule **Automatically request Copilot code review**; its reviews don't count toward required approvals unless Copilot approvals are enabled at repo, org and enterprise level.
- Azure Repos (GA 20 Nov 2026): enable under Organization settings → Repos → Repositories, then branch policy **Automatically request Copilot code review**. Always a **Comment** review; never approves or blocks. Runs as pipeline jobs on the default pool (no self-hosted) ([blog](https://devblogs.microsoft.com/devops/copilot-code-reviews-for-azure-repos-is-generally-available/)).

**Quick commands**
```bash
# Azure DevOps: protect main (needs repo GUID), then list.
az repos policy approver-count create --repository-id $REPO_ID --branch main --blocking true --enabled true --minimum-approver-count 1 --creator-vote-counts true --allow-downvotes false --reset-on-source-push true
az repos policy list --repository-id $REPO_ID --branch main -o table
# GitHub: create a ruleset from JSON, inspect effective rules on main.
gh api --method POST repos/OWNER/REPO/rulesets --input ruleset.json
gh ruleset check main -R OWNER/REPO
```

**Exam traps:** release branches get **cherry-picks**, not merges · policies apply to the **target** branch · `prefix` match covers a folder · requester's approval on an agent PR doesn't count · agent checks stay pending until **Approve and run workflows** · Copilot review ≠ approval · `bypass_mode: pull_request` blocks direct pushes even for the bypass actor · multiple rulesets: strictest wins · `gh pr edit --body` bug → use `gh api --method PATCH`.
