import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(12, 15), dpi=150)
ax.set_xlim(0, 12); ax.set_ylim(0, 15); ax.axis("off")
fig.patch.set_facecolor("#0f1226")
def box(x,y,w,h,c,title,body,tc="white",fs=10.4):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.25",fc=c,ec="white",lw=1.5))
    ax.text(x+w/2,y+h-0.32,title,ha="center",va="top",fontsize=13,weight="bold",color=tc)
    ax.text(x+0.2,y+h-0.85,body,ha="left",va="top",fontsize=fs,color=tc,linespacing=1.45)
ax.text(6,14.6,"AZ-401  |  Day 4: Branching, PRs & Branch Rules",ha="center",fontsize=21,weight="bold",color="#FDCB6E")
ax.text(6,14.1,"Domain 2 · Source control (10–15%) · Fri 27 Nov 2026 · Exam Sun 13 Dec, 1:30 PM IST",ha="center",fontsize=10.5,color="#dfe6e9")
# strategy strip
stages=[("FEATURE","topic branch\n→ PR → main","#00B894"),("TRUNK","short-lived\n+ flags","#0984E3"),("RELEASE","release/NN\ncherry-pick","#e17055"),("WORKTREE","1 branch per\nfolder (tool)","#6C5CE7"),("GIT FLOW","main+develop\n2 merges","#d63031"),("GH FLOW","branch→PR→\nmerge→deploy","#e84393")]
xs=[0.3,2.25,4.2,6.15,8.1,10.05]
for (t,s,c),x in zip(stages,xs):
    ax.add_patch(FancyBboxPatch((x,12.0),1.65,1.4,boxstyle="round,pad=0.05,rounding_size=0.3",fc=c,ec="white",lw=1.5))
    ax.text(x+0.825,13.0,t,ha="center",fontsize=11.5,weight="bold",color="white")
    ax.text(x+0.825,12.5,s,ha="center",va="center",fontsize=9.2,color="white",linespacing=1.3)
ax.text(6,11.45,"Keep it simple: feature branches · PRs only · protected, always-buildable main · fix on main, cherry-pick to release",ha="center",fontsize=10,color="#FDCB6E",style="italic")
box(0.3,6.6,5.5,4.4,"#0078D4","Azure Repos: branch policies",
"az repos policy approver-count | work-item-linking\n   comment-required | merge-strategy | build\n   required-reviewer (path filter must start with /)\nScope: --branch main  or  release/ + prefix\nEvaluated on the TARGET branch\nRequired (blocking) vs Optional\nBypass = permission (complete PR / push)\nCan't delete a branch with required policies\nCopilot review policy: Comment only (GA 20 Nov)",fs=11.4)
box(6.2,6.6,5.5,4.4,"#24292f","GitHub: rulesets vs classic",
"Rulesets stack: MOST RESTRICTIVE wins\nactive | disabled  (evaluate = Enterprise)\nbypass_actors: Admin role id 5\n   always | pull_request | exempt\nRules: pull_request (0-10 approvals)\n   status checks · merge_queue · linear history\n   copilot_code_review · code_scanning\nClassic: ONE rule per branch,\n   admins bypass unless enforced\ngh api --method POST repos/o/r/rulesets",fs=11.4)
box(0.3,2.7,11.4,3.6,"#4834d4","Copilot cloud agent PR rules (GitHub)",
"Only WRITE users can trigger · pushes to ONE branch: copilot/…  (or the PR branch on @copilot)\nDraft PR · agent can't mark ready, approve or merge · commits signed, you are co-author\nWorkflows wait for a writer to click  Approve and run workflows  (required checks stay pending)\nRequester CAN'T approve → another reviewer · PR under Copilot's own identity = +1 approval (default on)\nStill bound by rulesets and required checks · Copilot code review = advisory, not an approval (default)",fs=11.4)
ax.add_patch(FancyBboxPatch((0.3,0.35),11.4,2.05,boxstyle="round,pad=0.08,rounding_size=0.25",fc="#2d3436",ec="#FDCB6E",lw=2))
ax.text(6,2.05,"Today's lab (≈ ₹0, no Azure resources)",ha="center",fontsize=13,weight="bold",color="#FDCB6E")
ax.text(6,1.2,"A: scratch repo: squash merge · release/1.0 · cherry-pick -x · git worktree add/remove\n"
"B: ADO az repos policy: reviewers · comments · squash-only · release/ prefix → direct push fails, PR passes\n"
"C: gh api rulesets (main-pr-review, copilot review, release/**) → human PR blocked → Copilot PR:\n"
"draft · Approve and run workflows · own approval doesn't count",ha="center",va="center",fontsize=9.6,color="white",linespacing=1.5)
plt.savefig("infographic.png",bbox_inches="tight",facecolor=fig.get_facecolor())
