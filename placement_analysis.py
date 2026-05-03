import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — works without a display
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.ticker import FuncFormatter

# ─────────────────────────────────────────────
#  THEME & PALETTE
# ─────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0f1117",
    "axes.facecolor":    "#1a1d27",
    "axes.edgecolor":    "#2e3250",
    "axes.labelcolor":   "#c9d1d9",
    "axes.titlecolor":   "#ffffff",
    "axes.titlesize":    13,
    "axes.labelsize":    10,
    "axes.grid":         True,
    "grid.color":        "#2e3250",
    "grid.linestyle":    "--",
    "grid.alpha":        0.6,
    "xtick.color":       "#8b949e",
    "ytick.color":       "#8b949e",
    "text.color":        "#c9d1d9",
    "legend.facecolor":  "#1a1d27",
    "legend.edgecolor":  "#2e3250",
    "font.family":       "DejaVu Sans",
})

PALETTE   = ["#7c6af7", "#56cfb2", "#f7a35c", "#e05c8a", "#4fc3f7", "#a8e063"]
ACCENT    = "#7c6af7"
POSITIVE  = "#56cfb2"
NEGATIVE  = "#e05c8a"
HIGHLIGHT = "#f7a35c"

# ─────────────────────────────────────────────
#  LOAD & CLEAN DATA
# ─────────────────────────────────────────────
data = pd.read_csv("placement_data.csv")
placed     = data[data["Placed"] == "Yes"].copy()
not_placed = data[data["Placed"] == "No"].copy()

# ─────────────────────────────────────────────
#  CONSOLE SUMMARY
# ─────────────────────────────────────────────
total        = len(data)
total_placed = len(placed)
placement_pct = round((total_placed / total) * 100, 1)
highest_sal  = placed["Salary_LPA"].max()
avg_sal      = round(placed["Salary_LPA"].mean(), 2)
median_sal   = placed["Salary_LPA"].median()
top_company  = placed["Company"].value_counts().idxmax()
top_dept     = (placed.groupby("Department").size() / data.groupby("Department").size() * 100).idxmax()

print("=" * 55)
print("       CAMPUS PLACEMENT ANALYSIS REPORT")
print("=" * 55)
print(f"  Total Students       : {total}")
print(f"  Students Placed      : {total_placed}  ({placement_pct}%)")
print(f"  Students Not Placed  : {len(not_placed)}")
print(f"  Highest Salary       : {highest_sal} LPA")
print(f"  Average Salary       : {avg_sal} LPA")
print(f"  Median Salary        : {median_sal} LPA")
print(f"  Top Hiring Company   : {top_company}")
print(f"  Best Placed Dept     : {top_dept}")
print("=" * 55)

# Department stats
dept_total  = data.groupby("Department").size()
dept_placed = placed.groupby("Department").size()
dept_rate   = (dept_placed / dept_total * 100).round(1).fillna(0)
dept_avg_sal = placed.groupby("Department")["Salary_LPA"].mean().round(2)

print("\n  Department-wise Breakdown")
print(f"  {'Dept':<8} {'Total':>6} {'Placed':>7} {'Rate':>7} {'Avg Sal':>9}")
print("  " + "-" * 42)
for dept in dept_total.index:
    t  = dept_total.get(dept, 0)
    p  = dept_placed.get(dept, 0)
    r  = dept_rate.get(dept, 0)
    s  = dept_avg_sal.get(dept, 0)
    print(f"  {dept:<8} {t:>6} {p:>7} {r:>6}% {s:>8} LPA")

print("\n  Top 5 Highest Packages")
print(f"  {'Name':<12} {'Dept':<8} {'Company':<20} {'Salary':>8}")
print("  " + "-" * 52)
for _, row in placed.nlargest(5, "Salary_LPA").iterrows():
    print(f"  {row['Name']:<12} {row['Department']:<8} {row['Company']:<20} {row['Salary_LPA']:>6} LPA")
print("=" * 55)

# ─────────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────────
def bar_labels(ax, fmt="{:.0f}", color="#ffffff", fontsize=8.5):
    for bar in ax.patches:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + ax.get_ylim()[1] * 0.01,
                fmt.format(h),
                ha="center", va="bottom",
                fontsize=fontsize, color=color, fontweight="bold"
            )

# ─────────────────────────────────────────────
#  FIGURE 1 — OVERVIEW DASHBOARD (2×3 grid)
# ─────────────────────────────────────────────
fig1 = plt.figure(figsize=(20, 13))
fig1.patch.set_facecolor("#0f1117")
fig1.suptitle("Campus Placement Analysis Dashboard", fontsize=20,
              fontweight="bold", color="#ffffff", y=0.98)

gs = gridspec.GridSpec(2, 3, figure=fig1, hspace=0.45, wspace=0.35)

# ── 1. Placement Status Donut ──────────────────
ax1 = fig1.add_subplot(gs[0, 0])
sizes  = [total_placed, len(not_placed)]
colors = [POSITIVE, NEGATIVE]
wedges, texts, autotexts = ax1.pie(
    sizes, labels=["Placed", "Not Placed"],
    colors=colors, autopct="%1.1f%%",
    startangle=90, pctdistance=0.78,
    wedgeprops=dict(width=0.55, edgecolor="#0f1117", linewidth=2)
)
for t in texts:      t.set_color("#c9d1d9"); t.set_fontsize(10)
for at in autotexts: at.set_color("#ffffff"); at.set_fontsize(10); at.set_fontweight("bold")
ax1.set_title("Overall Placement Status", pad=14)
ax1.text(0, 0, f"{placement_pct}%", ha="center", va="center",
         fontsize=18, fontweight="bold", color="#ffffff")

# ── 2. Department Placement Rate ───────────────
ax2 = fig1.add_subplot(gs[0, 1])
colors_dept = [PALETTE[i % len(PALETTE)] for i in range(len(dept_rate))]
bars = ax2.bar(dept_rate.index, dept_rate.values, color=colors_dept,
               edgecolor="#0f1117", linewidth=1.2, width=0.55)
ax2.set_title("Department-wise Placement Rate")
ax2.set_ylabel("Placement %")
ax2.set_ylim(0, 115)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
bar_labels(ax2, fmt="{:.0f}%")

# ── 3. Average Salary by Department ───────────
ax3 = fig1.add_subplot(gs[0, 2])
dept_avg_sorted = dept_avg_sal.sort_values(ascending=False)
colors_sal = [PALETTE[i % len(PALETTE)] for i in range(len(dept_avg_sorted))]
ax3.barh(dept_avg_sorted.index, dept_avg_sorted.values,
         color=colors_sal, edgecolor="#0f1117", linewidth=1.2, height=0.55)
ax3.set_title("Avg Salary by Department (LPA)")
ax3.set_xlabel("Salary (LPA)")
ax3.invert_yaxis()
for i, (val, dept) in enumerate(zip(dept_avg_sorted.values, dept_avg_sorted.index)):
    ax3.text(val + 0.2, i, f"{val:.1f}", va="center",
             fontsize=9, color="#ffffff", fontweight="bold")

# ── 4. Top 10 Companies ────────────────────────
ax4 = fig1.add_subplot(gs[1, 0:2])
company_count = placed["Company"].value_counts().head(10)
colors_comp   = [PALETTE[i % len(PALETTE)] for i in range(len(company_count))]
bars4 = ax4.bar(company_count.index, company_count.values,
                color=colors_comp, edgecolor="#0f1117", linewidth=1.2, width=0.6)
ax4.set_title("Top 10 Companies by Hiring Count")
ax4.set_ylabel("Students Hired")
ax4.set_ylim(0, company_count.max() + 2)
plt.setp(ax4.get_xticklabels(), rotation=30, ha="right", fontsize=9)
bar_labels(ax4)

# ── 5. Salary Distribution Histogram ──────────
ax5 = fig1.add_subplot(gs[1, 2])
sal_vals = placed["Salary_LPA"]
n, bins, patches = ax5.hist(sal_vals, bins=10, color=ACCENT,
                             edgecolor="#0f1117", linewidth=1.2, alpha=0.85)
ax5.axvline(avg_sal,    color=HIGHLIGHT, linestyle="--", linewidth=1.8, label=f"Mean: {avg_sal}")
ax5.axvline(median_sal, color=POSITIVE,  linestyle=":",  linewidth=1.8, label=f"Median: {median_sal}")
ax5.set_title("Salary Distribution (Placed Students)")
ax5.set_xlabel("Salary (LPA)")
ax5.set_ylabel("Number of Students")
ax5.legend(fontsize=9)

plt.savefig("dashboard_overview.png", dpi=150, bbox_inches="tight",
            facecolor=fig1.get_facecolor())
print("  ✔  Saved dashboard_overview.png")
plt.close(fig1)

# ─────────────────────────────────────────────
#  FIGURE 2 — DEEP DIVE (2×2 grid)
# ─────────────────────────────────────────────
fig2 = plt.figure(figsize=(18, 12))
fig2.patch.set_facecolor("#0f1117")
fig2.suptitle("Deep Dive — Skills, CGPA & Gender Insights", fontsize=18,
              fontweight="bold", color="#ffffff", y=0.98)

gs2 = gridspec.GridSpec(2, 2, figure=fig2, hspace=0.45, wspace=0.35)

# ── 6. CGPA vs Salary Scatter ─────────────────
ax6 = fig2.add_subplot(gs2[0, 0])
dept_list   = placed["Department"].unique()
dept_colors = {d: PALETTE[i % len(PALETTE)] for i, d in enumerate(dept_list)}
for dept in dept_list:
    sub = placed[placed["Department"] == dept]
    ax6.scatter(sub["CGPA"], sub["Salary_LPA"],
                color=dept_colors[dept], s=70, alpha=0.85,
                edgecolors="#0f1117", linewidth=0.8, label=dept)
# Trend line
z = np.polyfit(placed["CGPA"], placed["Salary_LPA"], 1)
p = np.poly1d(z)
x_line = np.linspace(placed["CGPA"].min(), placed["CGPA"].max(), 100)
ax6.plot(x_line, p(x_line), color=HIGHLIGHT, linewidth=2,
         linestyle="--", label="Trend", zorder=5)
ax6.set_title("CGPA vs Salary (LPA)")
ax6.set_xlabel("CGPA")
ax6.set_ylabel("Salary (LPA)")
ax6.legend(fontsize=8, ncol=2)

# ── 7. Gender-wise Placement ──────────────────
ax7 = fig2.add_subplot(gs2[0, 1])
gender_placed = data.groupby(["Gender", "Placed"]).size().unstack(fill_value=0)
x      = np.arange(len(gender_placed.index))
width  = 0.35
b1 = ax7.bar(x - width/2, gender_placed.get("Yes", 0), width,
             label="Placed",     color=POSITIVE, edgecolor="#0f1117", linewidth=1.2)
b2 = ax7.bar(x + width/2, gender_placed.get("No", 0),  width,
             label="Not Placed", color=NEGATIVE, edgecolor="#0f1117", linewidth=1.2)
ax7.set_title("Gender-wise Placement Comparison")
ax7.set_ylabel("Number of Students")
ax7.set_xticks(x)
ax7.set_xticklabels(gender_placed.index)
ax7.legend(fontsize=9)
ax7.set_ylim(0, gender_placed.values.max() + 5)
for bar in list(b1) + list(b2):
    h = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2, h + 0.3, str(int(h)),
             ha="center", va="bottom", fontsize=9, color="#ffffff", fontweight="bold")

# ── 8. Internship Impact ──────────────────────
ax8 = fig2.add_subplot(gs2[1, 0])
intern_rate = data.groupby("Internship").apply(
    lambda x: (x["Placed"] == "Yes").sum() / len(x) * 100,
    include_groups=False
).round(1)
colors_intern = [NEGATIVE, POSITIVE]
bars8 = ax8.bar(["No Internship", "Had Internship"],
                intern_rate.values, color=colors_intern,
                edgecolor="#0f1117", linewidth=1.2, width=0.45)
ax8.set_title("Internship Impact on Placement Rate")
ax8.set_ylabel("Placement Rate (%)")
ax8.set_ylim(0, 115)
ax8.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
for bar in bars8:
    h = bar.get_height()
    ax8.text(bar.get_x() + bar.get_width()/2, h + 1.5,
             f"{h:.1f}%", ha="center", va="bottom",
             fontsize=12, color="#ffffff", fontweight="bold")

# ── 9. CGPA Band Analysis ─────────────────────
ax9 = fig2.add_subplot(gs2[1, 1])
bins_cgpa  = [0, 6, 7, 8, 9, 10]
labels_cgpa = ["<6.0", "6–7", "7–8", "8–9", "9–10"]
data["CGPA_Band"] = pd.cut(data["CGPA"], bins=bins_cgpa, labels=labels_cgpa)
band_total  = data.groupby("CGPA_Band", observed=True).size()
band_placed = data[data["Placed"] == "Yes"].groupby("CGPA_Band", observed=True).size()
band_rate   = (band_placed / band_total * 100).fillna(0).round(1)

colors_band = [PALETTE[i % len(PALETTE)] for i in range(len(band_rate))]
bars9 = ax9.bar(band_rate.index.astype(str), band_rate.values,
                color=colors_band, edgecolor="#0f1117", linewidth=1.2, width=0.55)
ax9.set_title("Placement Rate by CGPA Band")
ax9.set_xlabel("CGPA Range")
ax9.set_ylabel("Placement Rate (%)")
ax9.set_ylim(0, 115)
ax9.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
for bar in bars9:
    h = bar.get_height()
    ax9.text(bar.get_x() + bar.get_width()/2, h + 1.5,
             f"{h:.0f}%", ha="center", va="bottom",
             fontsize=10, color="#ffffff", fontweight="bold")

plt.savefig("dashboard_deepdive.png", dpi=150, bbox_inches="tight",
            facecolor=fig2.get_facecolor())
print("  ✔  Saved dashboard_deepdive.png")
plt.close(fig2)

print("\n  Charts saved → dashboard_overview.png & dashboard_deepdive.png")
print("=" * 55)
