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
ax.text(6,14.6,"AZ-401  |  Day 3: Agentic Collaboration & Integrations",ha="center",fontsize=21,weight="bold",color="#FDCB6E")
ax.text(6,14.1,"Domain 1 · Processes & communications (15–20%) · Thu 26 Nov 2026 · Exam Sun 13 Dec, 1:30 PM IST",ha="center",fontsize=10.5,color="#dfe6e9")
# agent loop flow
stages=[("INSTRUCT","copilot-instructions\nAGENTS.md","#6C5CE7"),("RESTRICT","agent tools:\nallow-list","#d63031"),("CONNECT","MCP: ADO +\nGitHub","#0984E3"),("ACT","plan → tool →\nobserve","#00B894"),("REVIEW","draft PR ·\nhuman merges","#FDCB6E")]
xs=[0.4,2.75,5.1,7.45,9.8]
for (t,s,c),x in zip(stages,xs):
    ax.add_patch(FancyBboxPatch((x,12.0),1.85,1.4,boxstyle="round,pad=0.05,rounding_size=0.3",fc=c,ec="white",lw=1.5))
    col="#222" if t=="REVIEW" else "white"
    ax.text(x+0.925,13.0,t,ha="center",fontsize=12.5,weight="bold",color=col)
    ax.text(x+0.925,12.55,s,ha="center",va="center",fontsize=8.6,color=col,linespacing=1.3)
for i in range(4):
    ax.add_patch(FancyArrowPatch((xs[i]+1.9,12.7),(xs[i+1]-0.05,12.7),arrowstyle="-|>",mutation_scale=18,color="white",lw=2))
ax.add_patch(FancyArrowPatch((10.7,11.95),(1.3,11.95),connectionstyle="arc3,rad=-0.12",arrowstyle="-|>",mutation_scale=18,color="#FDCB6E",lw=2))
ax.text(6,11.0,"instructions GUIDE the model · tools / rulesets / CI checks ENFORCE",ha="center",fontsize=9.5,color="#FDCB6E",style="italic")
box(0.3,6.3,5.5,4.3,"#4834d4","Agent requirements as code",
".github/copilot-instructions.md  (repo-wide)\n.github/instructions/*.instructions.md\n   applyTo: \"glob\" · excludeAgent\nAGENTS.md  (nearest file wins)\n.github/agents/NAME.agent.md\n   description required · tools allow-list\n   [] = none · omitted / [\"*\"] = all\n.github/skills/NAME/SKILL.md (on demand)\n.github/hooks/*.json  preToolUse can deny",fs=10.6)
box(6.2,6.3,5.5,4.3,"#0652DD","MCP servers",
"ADO remote (GA): mcp.dev.azure.com/{org}\n   Entra OAuth only · X-MCP-Toolsets\n   X-MCP-Readonly · needs agent mode\nADO local: npx -y @azure-devops/mcp {org}\n   -d domains · -a azcli|pat|interactive\nGitHub: api.githubcopilot.com/mcp/\n   default: context,repos,issues,\n   pull_requests,users · /readonly · /x/…",fs=10.6)
box(0.3,2.6,5.5,3.4,"#00896b","Where MCP is configured",
"VS Code: .vscode/mcp.json\n   { servers, inputs } · you approve tools\nCloud agent: Settings → Copilot → MCP\n   { mcpServers } · tools REQUIRED\n   COPILOT_MCP_* Agents secrets\n   no OAuth remotes → ADO = local + azcli",fs=10.6)
box(6.2,2.6,5.5,3.4,"#b33939","Service hooks vs webhooks",
"ADO: POST _apis/hooks/subscriptions\n   tfs · workitem.created / build.complete\n   webHooks/httpRequest · Project Admin\n   HTTPS · basic auth/headers · no signature\nGitHub: POST /repos/{o}/{r}/hooks\n   content_type json · secret → HMAC\n   X-Hub-Signature-256 · constant-time",fs=10.6)
ax.add_patch(FancyBboxPatch((0.3,0.35),11.4,1.9,boxstyle="round,pad=0.08,rounding_size=0.25",fc="#2d3436",ec="#FDCB6E",lw=2))
ax.text(6,1.95,"Today's lab (≈ ₹0, no Azure resources)",ha="center",fontsize=13,weight="bold",color="#FDCB6E")
ax.text(6,1.1,"A: instructions + AGENTS.md + boards-triage / docs-writer agents (+ skill) → PR AB#id\n"
"B: .vscode/mcp.json ADO + GitHub → story + issue via MCP   C: cloud agent + Learn MCP → draft PR\n"
"D: ADO service hooks → webhook.site   E: gh api repo webhook + HMAC verify\n"
"Free: MCP servers, service hooks, webhooks, Learn MCP · Cloud agent uses premium requests · Clean up only what the lab created",ha="center",va="center",fontsize=8.6,color="white",linespacing=1.6)
ax.text(6,0.08,"Sources: AZ-401 study guide · GitHub Copilot customization & MCP docs · Azure DevOps MCP Server docs · ADO service hooks · GitHub webhooks docs",ha="center",fontsize=7.5,color="#b2bec3")
plt.savefig("infographic.png",facecolor=fig.get_facecolor(),bbox_inches="tight")
