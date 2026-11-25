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
ax.text(6,14.6,"AZ-401  |  Day 2: Success Metrics & Docs-as-Code",ha="center",fontsize=21,weight="bold",color="#FDCB6E")
ax.text(6,14.1,"Domain 1 · Processes & communications (15–20%) · Wed 25 Nov 2026 · Exam Sun 13 Dec, 1:30 PM IST",ha="center",fontsize=10.5,color="#dfe6e9")
# KPI -> metric flow
stages=[("KPI","business goal","#6C5CE7"),("METRIC","definition + target","#00B894"),("SOURCE","Analytics / runs","#0984E3"),("WIDGET","dashboard · OData","#E17055"),("REVIEW","retro → backlog","#FDCB6E")]
xs=[0.4,2.75,5.1,7.45,9.8]
for (t,s,c),x in zip(stages,xs):
    ax.add_patch(FancyBboxPatch((x,12.0),1.85,1.4,boxstyle="round,pad=0.05,rounding_size=0.3",fc=c,ec="white",lw=1.5))
    col="#222" if t=="REVIEW" else "white"
    ax.text(x+0.925,12.95,t,ha="center",fontsize=12.5,weight="bold",color=col)
    ax.text(x+0.925,12.4,s,ha="center",fontsize=8.6,color=col)
for i in range(4):
    ax.add_patch(FancyArrowPatch((xs[i]+1.9,12.7),(xs[i+1]-0.05,12.7),arrowstyle="-|>",mutation_scale=18,color="white",lw=2))
ax.add_patch(FancyArrowPatch((10.7,11.95),(3.65,11.95),connectionstyle="arc3,rad=-0.12",arrowstyle="-|>",mutation_scale=18,color="#FDCB6E",lw=2))
ax.text(7.2,11.05,"adjust the target, not the data  (Goodhart: a metric is not the goal)",ha="center",fontsize=9.5,color="#FDCB6E",style="italic")
box(0.3,6.9,5.5,3.8,"#00896b","DORA: now FIVE metrics",
"THROUGHPUT\n  • Change lead time (commit → prod)\n  • Deployment frequency\n  • Failed deployment recovery time\n     (replaced MTTR)\nINSTABILITY\n  • Change fail rate\n  • Deployment rework rate")
box(6.2,6.9,5.5,3.8,"#4834d4","Boards flow widgets",
"Lead time  = created → Completed\nCycle time = 1st In Progress → final Completed\n  (reactivations included in the span)\nCFD = items per column → bottlenecks, WIP\nVelocity = credit to sprint COMPLETED in\nOnly backlog WITs · Boards off = no widgets\n≠ DORA change lead time (starts at commit)")
box(0.3,2.6,5.5,3.9,"#0652DD","Analytics / OData + AI",
"analytics.dev.azure.com/{org}/{proj}/_odata/\n   v3.0-preview/WorkItems  (v2.0 = released)\n$apply=filter()/groupby()/aggregate(\n   CycleTimeDays with average as Avg)\nToken: az account get-access-token\n   --resource 499b84ac-…-267ca6975798\nAnalytics views = Boards only, flat\nAI: ADO MCP (wit,work · read-only) → check OData",fs=9.9)
box(6.2,2.6,5.5,3.9,"#b33939","Docs-as-code with Copilot",
"CODEOWNERS: .github/ → root → docs/\n  last match wins · base branch · write access\nrelease.yml: categories by label, \"*\" catch-all\n  gh release create v0.1.0 --generate-notes\nLICENSE in root · no license = all rights\nADO code wiki: .order · versioned · 'graph'\nPrompt files .github/prompts · cloud agent",fs=9.9)
ax.add_patch(FancyBboxPatch((0.3,0.35),11.4,1.9,boxstyle="round,pad=0.08,rounding_size=0.25",fc="#2d3436",ec="#FDCB6E",lw=2))
ax.text(6,1.95,"Today's lab (≈ ₹0, no Azure resources)",ha="center",fontsize=13,weight="bold",color="#FDCB6E")
ax.text(6,1.15,"ADO: az boards work-item update --state Active/Closed → Cycle/Lead/CFD widgets → OData via curl + Entra token → code wiki + Mermaid\n"
"GitHub: .github/CODEOWNERS + release.yml → /changelog prompt file → PR 'Fixes AB#id' → gh release create --generate-notes\n"
"Free: Analytics, widgets, wiki, ADO MCP · Optional cloud agent uses premium requests · Clean up yourself",ha="center",va="center",fontsize=8.6,color="white",linespacing=1.6)
ax.text(6,0.08,"Sources: AZ-401 study guide · dora.dev metrics guide · ADO Analytics/OData & widget docs · GitHub CODEOWNERS & release-notes docs",ha="center",fontsize=7.5,color="#b2bec3")
plt.savefig("infographic.png",facecolor=fig.get_facecolor(),bbox_inches="tight")
