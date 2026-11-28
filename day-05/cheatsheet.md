# Day 5 Cheat Sheet: Repo permissions, tags, traceability, Git hooks, GEI migration, recovering/removing data (Domain 2, 10–15%)

**Permissions** ([Azure Repos](https://learn.microsoft.com/en-us/azure/devops/repos/git/set-git-repository-permissions?view=azure-devops), [namespaces](https://learn.microsoft.com/en-us/azure/devops/organizations/security/namespace-reference?view=azure-devops), [CLI](https://learn.microsoft.com/en-us/cli/azure/devops/security/permission?view=azure-cli-latest), [GitHub roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization))

| Azure Repos | GitHub |
|---|---|
| Allow / Deny / Not set; inherit **All Repositories → repo → branch/tag**; Deny usually wins | Roles **Read → Triage → Moderate → Write → Maintain → Admin**; **custom roles** = Enterprise Cloud only (max 20) |
| Contributors: Contribute, Create branch, **Create tag**, Manage notes. **Force push** + **Bypass policies** = no group by default | Personal-account repo: owner + collaborators only |
| Branch creator gets Contribute, Force push, Manage permissions on that branch | `GET /repos/{o}/{r}/collaborators/{u}/permission` → `permission`, `role_name` |
| Namespace **Git Repositories** `2e9eb7ed-…fd87`; token `repoV2/<projId>/<repoId>` | Org base permission + teams + outside collaborators |
| `az devops security permission show|update --allow-bit/--deny-bit|reset|reset-all` (needs PCA) | Rulesets bypass: role, team, app, user |

**Tags** ([git-tag](https://git-scm.com/docs/git-tag), [ADO tags](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-tags?view=azure-devops), [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [sunset](https://github.blog/changelog/2024-05-29-sunset-notice-tag-protections/))
- Lightweight `git tag v1` (just a ref) · annotated `git tag -a v1 -m msg` (object: tagger, date, message) · signed `git tag -s` / verify `git tag -v`. `git describe` ignores lightweight tags. Push: `git push origin v1` / `--tags` / `--follow-tags`.
- ADO portal creates **annotated** tags. Create = **Create tag**, delete = **Force push** (tag creator has it).
- GitHub: tag protection rules were **sunset (Aug 2024)** → **tag rulesets** (`target: tag`, rules `creation`, `update`, `deletion`, `non_fast_forward`). A block shows `GH013`.

**Traceability** ([repo settings](https://learn.microsoft.com/en-us/azure/devops/repos/git/repository-settings?view=azure-devops), [AB#](https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops), [autolinks](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/configuring-autolinks-to-reference-external-resources), [PR coverage](https://learn.microsoft.com/en-us/azure/devops/pipelines/test/codecoverage-for-pullrequests?view=azure-devops), [Code Quality](https://docs.github.com/en/code-security/code-quality/concepts/about-code-quality))

| Need | Azure DevOps | GitHub |
|---|---|---|
| Commit → work item | `#123` (*Commit mention linking*; *work item resolution* with `Fixes #123`) | `AB#123` in commit / PR description / issue (not PR title or comments); `Fixes AB#123` transitions |
| Other trackers | n/a | **Autolinks**: `key_prefix` + `url_template` with `<num>` (plans: Pro, Team, Enterprise) |
| Coverage gate | Diff coverage status on PR, default **70 %**, `azurepipelines-coverage.yml`, Azure Repos only | Code Quality findings + coverage rule (preview) |

**Hooks: client vs server** ([githooks](https://git-scm.com/docs/githooks), [push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection), [push rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [GHAzDO](https://learn.microsoft.com/en-us/azure/devops/repos/security/github-advanced-security-secret-scanning?view=azure-devops), [Copilot hooks](https://docs.github.com/en/copilot/concepts/agents/hooks))
- Client: `pre-commit`, `commit-msg`, `pre-push` in `.git/hooks` or a shared folder via `git config core.hooksPath .githooks`. They must be **executable**, are **not cloned**, and are skipped by `--no-verify` → advisory only.
- Server (enforced): ADO **branch policies** + **push protection** (GHAzDO / Secret Protection for ADO; bypass `skip-secret-scanning:true`). GitHub **rulesets**, **push rulesets** (Team; `file_path_restriction`, `file_extension_restriction`, `max_file_size`, `max_file_path_length`), **push protection** (free on public repos; private needs Secret Protection). GHES only: **pre-receive hooks**.
- Copilot agent hooks: `.github/hooks/*.json`, `version: 1`, `preToolUse` can deny tool calls (on the default branch for the cloud agent).

**GEI: Azure DevOps → GitHub** ([guide](https://docs.github.com/en/migrations/using-github-enterprise-importer/migrating-from-azure-devops-to-github-enterprise-cloud), [access](https://docs.github.com/en/migrations/using-github-enterprise-importer/ado/manage-access), [follow-up](https://docs.github.com/en/migrations/using-github-enterprise-importer/ado/follow-up-tasks))
- ADO **Services (cloud)** → **GitHub Enterprise Cloud**. Install with `gh extension install github/gh-ado2gh` (gh 2.4.0+).
- **PATs only**: `GH_PAT` = **classic** (owner `repo, workflow, admin:org`; migrator `repo, workflow, read:org`). `ADO_PAT` Work Items/Code/Identity Read (Full access for inventory).
- Flow: `inventory-report` → `generate-script --github-org X [--all]` → trial in a `-sandbox` org → `migrate-repo` / `migrate.ps1` → `wait-for-migration` → follow-ups.
- Migrated ([about](https://docs.github.com/en/migrations/using-github-enterprise-importer/migrating-from-azure-devops-to-github-enterprise-cloud/about-migrations-from-azure-devops-to-github-enterprise-cloud)): Git source + history, PRs (user history, **work item links**, attachments), branch policies (not user-scoped or cross-repo). **Not**: LFS objects (push them afterwards), permissions. Pipelines and Boards stay in ADO and get **integrated**. Limits: 40 GiB repo, 400 MiB file during migration. Target name `<project>-<repo>`, **private**.
- Follow-ups: Migration Log issue, **reclaim mannequins**, teams `<proj>-Maintainers/-Admins`, `rewire-pipeline` (`--dry-run`), `integrate-boards`, `configure-autolink`, `lock-ado-repo` / `disable-ado-repo`.

**Recover / remove** ([undo](https://learn.microsoft.com/en-us/azure/devops/repos/git/undo?view=azure-devops), [restore branch](https://learn.microsoft.com/en-us/azure/devops/repos/git/restore-deleted-branch?view=azure-devops), [ADO recycle bin](https://learn.microsoft.com/en-us/azure/devops/repos/git/delete-existing-repo?view=azure-devops), [GitHub restore repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/restoring-a-deleted-repository), [sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository))

| Situation | Do this |
|---|---|
| Bad commit already pushed/shared | `git revert <sha>` (new commit, history intact) |
| Local only, not pushed | `git reset --soft|--mixed|--hard <ref>` |
| "Lost" commit after reset/rebase | `git reflog` → `git branch rescue <sha>` (unreachable entries kept 30 days, reachable 90) |
| Deleted branch, ADO | Branches → search exact name → **Restore branch** (no time limit; policies/permissions not restored) or `az repos ref create` |
| Deleted branch, GitHub | Closed PR → **Restore branch**, or activity API `branch_deletion` → `POST /git/refs` |
| Deleted repo | ADO recycle bin **30 days** (REST `PATCH …/recycleBin/repositories/{id}` `{"deleted":false}`); GitHub **90 days** |
| Secret committed | **1. Rotate/revoke** → 2. fresh clone → `git filter-repo --sensitive-data-removal --replace-text r.txt` / `--invert-paths --path f` (2.47+) → 3. `git push --force --mirror` (lift tag/branch protections first) → 4. GitHub Support for PR refs/cached views → 5. everyone re-clones |
