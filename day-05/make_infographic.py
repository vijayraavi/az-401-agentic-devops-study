import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(12, 15), dpi=150)
ax.set_xlim(0, 12); ax.set_ylim(0, 15); ax.axis("off")
fig.patch.set_facecolor("#0f1226")
def box(x,y,w,h,c,title,body,tc="white",fs=10.4):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.25",fc=c,ec="white",lw=1.5))
    ax.text(x+w/2,y+h-0.32,title,ha="center",va="top",fontsize=13,weight="bold",color=tc)
    ax.text(x+0.2,y+h-0.85,body,ha="left",va="top",fontsize=fs,color=tc,linespacing=1.45)
ax.text(6,14.6,"AZ-401  |  Day 5: Permissions, Tags, Hooks, GEI & Recovery",ha="center",fontsize=21,weight="bold",color="#FDCB6E")
ax.text(6,14.1,"Domain 2 · Source control (10–15%) · Sat 28 Nov 2026 · Exam Sun 13 Dec, 1:30 PM IST",ha="center",fontsize=10.5,color="#dfe6e9")
stages=[("PERMS","Allow/Deny\nRead→Admin","#00B894"),("TAGS","annotated\n+ rulesets","#0984E3"),("TRACE","#ID · AB#\nautolinks","#e17055"),("HOOKS","client = advisory\nserver = enforce","#6C5CE7"),("GEI","ADO → GHEC\nPATs only","#d63031"),("RECOVER","revert · reflog\nfilter-repo","#e84393")]
xs=[0.3,2.25,4.2,6.15,8.1,10.05]
for (t,s,c),x in zip(stages,xs):
    ax.add_patch(FancyBboxPatch((x,12.0),1.65,1.4,boxstyle="round,pad=0.05,rounding_size=0.3",fc=c,ec="white",lw=1.5))
    ax.text(x+0.825,13.0,t,ha="center",fontsize=11.5,weight="bold",color="white")
    ax.text(x+0.825,12.5,s,ha="center",va="center",fontsize=9,color="white",linespacing=1.3)
ax.text(6,11.45,"Leaked secret?  ROTATE first → filter-repo in a fresh clone → force-push --mirror → Support → re-clone",ha="center",fontsize=10.5,color="#FDCB6E",style="italic")
box(0.3,6.6,5.5,4.4,"#0078D4","Azure DevOps",
"Inherit All Repos → repo → branch/tag; Deny wins\nContributors: Contribute, Create branch/tag\nForce push + Bypass: no group by default\nDelete tag = Force push · portal = annotated\n#ID commit mention linking · diff coverage 70%\nPush protection = GHAzDO / Secret Protection\nDeleted branch: restore, no time limit\n   (policies + permissions NOT restored)\nRepo recycle bin 30 days (REST PATCH)",fs=11)
box(6.2,6.6,5.5,4.4,"#24292f","GitHub",
"Roles Read→Triage→Moderate→Write→\n   Maintain→Admin · custom = GHEC (20)\nTag protection sunset → TAG RULESETS\nAB#123 (Boards app) · autolinks <num>\nPush protection: free on public (GH013)\nPush rulesets (Team): path/ext/size\npre-receive hooks = GHES only\nRestore PR branch · deleted repo 90 days\nCopilot hooks: .github/hooks/*.json",fs=11)
box(0.3,2.7,11.4,3.6,"#4834d4","GEI: gh ado2gh (Azure DevOps Services → GitHub Enterprise Cloud)",
"PATs only: GH_PAT classic (owner repo, workflow, admin:org · migrator repo, workflow, read:org) + ADO_PAT\ninventory-report → generate-script --github-org X [--all] → trial in -sandbox org → migrate-repo\nMigrated: git history, PRs, work item links, PR attachments, branch policies · Not: LFS objects, permissions\nFollow-up: Migration Log issue · reclaim mannequins · private by default · rewire-pipeline\n   integrate-boards · configure-autolink · lock-ado-repo / disable-ado-repo",fs=10.8)
ax.add_patch(FancyBboxPatch((0.3,0.35),11.4,2.05,boxstyle="round,pad=0.08,rounding_size=0.25",fc="#2d3436",ec="#FDCB6E",lw=2))
ax.text(6,2.05,"Today's lab (≈ ₹0, no Azure resources)",ha="center",fontsize=13,weight="bold",color="#FDCB6E")
ax.text(6,1.2,"A: scratch repo: pre-commit + commit-msg via core.hooksPath · --no-verify · tags · reflog/revert/reset\n"
"B: ADO throwaway repo: Deny Create tag · #ID link · restore branch · filter-repo purge · recycle bin\n"
"C: GitHub throwaway repos: tag ruleset · autolink · purge + force-push · restore branch · push protection\n"
"D: gh ado2gh inventory-report + generate-script dry run (short-lived PAT, nothing migrated)",ha="center",va="center",fontsize=9.6,color="white",linespacing=1.5)
plt.savefig("infographic.png",bbox_inches="tight",facecolor=fig.get_facecolor())
