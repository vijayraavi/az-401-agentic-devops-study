import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(12, 15), dpi=150)
ax.set_xlim(0, 12); ax.set_ylim(0, 15); ax.axis("off")
fig.patch.set_facecolor("#0f1226")
def box(x,y,w,h,c,title,body,tc="white"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.25",fc=c,ec="white",lw=1.5))
    ax.text(x+w/2,y+h-0.32,title,ha="center",va="top",fontsize=13,weight="bold",color=tc)
    ax.text(x+0.2,y+h-0.85,body,ha="left",va="top",fontsize=9.6,color=tc,linespacing=1.45)
ax.text(6,14.6,"AZ-401  |  Day 1: Flow of Work & Traceability",ha="center",fontsize=21,weight="bold",color="#FDCB6E")
ax.text(6,14.1,"Domain 1 · Processes & communications (15–20%) · Tue 24 Nov 2026 · Exam Sun 13 Dec, 1:30 PM IST",ha="center",fontsize=10.5,color="#dfe6e9")
# loop
stages=[("PLAN","Boards / Issues","#6C5CE7"),("BUILD","Repos · PRs · CI","#00B894"),("DEPLOY","YAML stages · Actions","#0984E3"),("OPERATE","Monitor · SRE Agent","#E17055"),("FEEDBACK","Notify · Service hooks","#FDCB6E")]
xs=[0.4,2.75,5.1,7.45,9.8]
for (t,s,c),x in zip(stages,xs):
    ax.add_patch(FancyBboxPatch((x,12.0),1.85,1.4,boxstyle="round,pad=0.05,rounding_size=0.3",fc=c,ec="white",lw=1.5))
    col="#222" if t=="FEEDBACK" else "white"
    ax.text(x+0.925,12.95,t,ha="center",fontsize=12.5,weight="bold",color=col)
    ax.text(x+0.925,12.4,s,ha="center",fontsize=8.6,color=col)
for i in range(4):
    ax.add_patch(FancyArrowPatch((xs[i]+1.9,12.7),(xs[i+1]-0.05,12.7),arrowstyle="-|>",mutation_scale=18,color="white",lw=2))
ax.add_patch(FancyArrowPatch((10.7,11.95),(1.3,11.95),connectionstyle="arc3,rad=-0.12",arrowstyle="-|>",mutation_scale=18,color="#FDCB6E",lw=2))
ax.text(6,11.05,"feedback loop → new work items",ha="center",fontsize=9.5,color="#FDCB6E",style="italic")
box(0.3,6.9,5.5,3.8,"#4834d4","AB# linking rules",
"✔ Commit message, PR DESCRIPTION, issue description\n✘ PR TITLE or comments do NOT link\n• 'Fixes AB#123' → Resolved category\n   (Completed if no Resolved state)\n• 'Closed AB#123' → Closed state\n• Transitions ONLY on merge to default branch\n• 1 GitHub repo ↔ 1 Azure DevOps org")
box(6.2,6.9,5.5,3.8,"#00896b","Enforce traceability",
"Azure Repos:\n  Branch policy 'Check for linked work items'\n  az repos policy work-item-linking create\n    --blocking true --branch main\nGitHub:\n  Ruleset → require PR + status check\n  Actions job greps PR body for AB#\\d+\n  (pass body via env:, permissions: read)")
box(0.3,2.6,5.5,3.9,"#0652DD","Agentic: MCP servers",
"Azure DevOps remote MCP (GA)\n  https://mcp.dev.azure.com/{org}\n  Entra ID auth · Entra-backed org only\n  X-MCP-Toolsets: wit,repos · X-MCP-Readonly\nGitHub remote MCP\n  https://api.githubcopilot.com/mcp/\n  OAuth/PAT · /readonly · toolsets\n→ Copilot agent mode links work ↔ code")
box(6.2,2.6,5.5,3.9,"#b33939","Feedback & metrics",
"Notifications: personal / team / project\nService hooks: Teams, Slack, Web Hooks\nLead time  = created → done\nCycle time = in progress → done\nProcess: Basic | Agile (User Story)\n  | Scrum (PBI) | CMMI (Requirement)")
ax.add_patch(FancyBboxPatch((0.3,0.35),11.4,1.9,boxstyle="round,pad=0.08,rounding_size=0.25",fc="#2d3436",ec="#FDCB6E",lw=2))
ax.text(6,1.95,"Today's lab (≈ ₹0)",ha="center",fontsize=13,weight="bold",color="#FDCB6E")
ax.text(6,1.15,"ADO: az devops project create → az boards work-item create (Epic › Story › Task) → linked-work-item policy → az repos pr create --work-items\n"
"GitHub: Azure Boards app → traceability-gate workflow → ruleset required check → 'Fixes AB#id' → merge → Resolved\n"
"Free tiers: ADO 5 Basic users + 1,800 hosted min/mo · Empty tagged RG only · Clean up yourself",ha="center",va="center",fontsize=8.8,color="white",linespacing=1.6)
ax.text(6,0.08,"Sources: learn.microsoft.com AZ-401 study guide · Boards↔GitHub AB# docs · ADO remote MCP docs · github/github-mcp-server",ha="center",fontsize=7.5,color="#b2bec3")
plt.savefig("infographic.png",facecolor=fig.get_facecolor(),bbox_inches="tight")
