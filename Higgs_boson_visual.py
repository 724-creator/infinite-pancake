"""
Higgs Boson Visualisation
=========================
Simulates:
  1. A Higgs boson (H) propagating through a quantum field
  2. Spontaneous decay into a bottom-quark pair (b b̄)
  3. The underlying Higgs potential ("Mexican hat")

Dependencies: matplotlib, numpy  (pip install matplotlib numpy)
Run:          python higgs_boson.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.gridspec import GridSpec

# ── Colours ───────────────────────────────────────────────────────────────────
BG        = "#0a0a1a"
HIGGS_COL = "#ff6ec7"
BQUARK    = "#00e5ff"
BBAR      = "#ffd700"
FIELD_COL = "#3a1f6e"
BOX_COL   = "#12122a"
TEXT_COL  = "#ccccee"

# ── Layout: 2 rows × 2 cols ───────────────────────────────────────────────────
#   [0,0] animation   [0,1] potential plot
#   [1,0] explanation [1,1] explanation
fig = plt.figure(figsize=(14, 9), facecolor=BG)
fig.suptitle("Higgs Boson  |  Production · Propagation · Decay",
             color="white", fontsize=14, fontweight="bold", y=0.98)

gs = GridSpec(2, 2, figure=fig,
              height_ratios=[3.2, 1],
              hspace=0.08, wspace=0.35)

ax_main  = fig.add_subplot(gs[0, 0])
ax_pot   = fig.add_subplot(gs[0, 1])
ax_exp1  = fig.add_subplot(gs[1, 0])
ax_exp2  = fig.add_subplot(gs[1, 1])

for ax in (ax_main, ax_pot, ax_exp1, ax_exp2):
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor("#1e1e40")

# ── Helper: plain-English explanation box ─────────────────────────────────────
def explanation_box(ax, title, lines, title_col=HIGGS_COL):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    box = FancyBboxPatch((0.01, 0.04), 0.98, 0.92,
                         boxstyle="round,pad=0.02",
                         facecolor=BOX_COL, edgecolor="#2a2a55",
                         linewidth=1.2, zorder=0)
    ax.add_patch(box)
    ax.text(0.5, 0.84, title,
            color=title_col, fontsize=10, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes, zorder=2)
    y_positions = np.linspace(0.64, 0.12, len(lines))
    for y, line in zip(y_positions, lines):
        ax.text(0.04, y, f"• {line}",
                color=TEXT_COL, fontsize=8.2,
                ha="left", va="center", transform=ax.transAxes, zorder=2)

# ── Explanation: animation panel ─────────────────────────────────────────────
explanation_box(
    ax_exp1,
    title="What you're watching  ↑",
    lines=[
        "The pink dot is the Higgs boson — a real particle first detected at CERN in 2012.",
        "It moves through the Higgs field (the wavy purple lines that fill all of space).",
        "After an incredibly short time it 'decays' — it breaks apart into two new particles:",
        "a bottom quark (cyan ↗) and its antimatter twin, the anti-bottom quark (gold ↘).",
        "This is the most common fate of a Higgs boson — it happens ~58% of the time.",
    ],
    title_col=HIGGS_COL,
)

# ── Explanation: potential panel ─────────────────────────────────────────────
explanation_box(
    ax_exp2,
    title="What the graph shows  ↑",
    lines=[
        "This curve shows the energy of the Higgs field — think of it as a landscape.",
        "The two dips (like the brim of a sombrero hat) are the lowest-energy spots.",
        "Just after the Big Bang the universe 'rolled' into one of those dips.",
        "That gave the Higgs field a non-zero value everywhere in space — even in a vacuum.",
        "Every particle with mass (electrons, quarks, you) gets that mass by pushing against this field.",
    ],
    title_col="#aaaaff",
)

# ── Higgs potential plot ──────────────────────────────────────────────────────
ax_pot.set_title("The Higgs Potential  (an energy landscape)", color="white", fontsize=10)
phi      = np.linspace(-2.2, 2.2, 400)
mu2, lam = -1.0, 0.5
V        = mu2 * phi**2 + lam * phi**4
ax_pot.plot(phi, V, color=HIGGS_COL, linewidth=2.5)
ax_pot.axhline(min(V), color="#444466", linewidth=0.8, linestyle="--")
ax_pot.set_xlabel("Higgs field strength  →", color="#aaaacc", fontsize=8)
ax_pot.set_ylabel("Energy  →", color="#aaaacc", fontsize=8)
ax_pot.tick_params(colors="#aaaacc", labelsize=7)

phi_min = np.sqrt(-mu2 / (2 * lam))
V_min   = mu2 * phi_min**2 + lam * phi_min**4
ax_pot.plot([phi_min, -phi_min], [V_min, V_min], "o",
            color=HIGGS_COL, markersize=8, zorder=5)

ax_pot.annotate("← Universe settled\n   into one of\n   these dips",
                xy=(-phi_min, V_min), xytext=(-1.9, -0.08),
                color="#ddddff", fontsize=7.5,
                arrowprops=dict(arrowstyle="->", color="#aaaacc", lw=0.9))
ax_pot.annotate("Unstable top\n(field = 0 here)",
                xy=(0, 0), xytext=(0.2, 0.22),
                color="#aaaacc", fontsize=7,
                arrowprops=dict(arrowstyle="->", color="#aaaacc", lw=0.8))

# ── Animation panel setup ─────────────────────────────────────────────────────
ax_main.set_title("Higgs Boson: Propagation & Decay  (H⁰ → b b̄)", color="white", fontsize=10)
ax_main.set_xlim(-1, 11)
ax_main.set_ylim(-3, 3)
ax_main.set_aspect("equal")
ax_main.set_xlabel("Space  →", color="#aaaacc", fontsize=8)
ax_main.tick_params(colors="#aaaacc")
ax_main.set_yticks([])

x_field = np.linspace(-1, 11, 300)
for k, y0 in enumerate(np.linspace(-2.5, 2.5, 14)):
    phase  = k * 0.45
    y_wave = y0 + 0.18 * np.sin(3 * x_field + phase)
    ax_main.plot(x_field, y_wave, color=FIELD_COL, linewidth=0.6, alpha=0.55)
ax_main.text(-0.85, 2.75, "Higgs\nfield", color="#5555aa", fontsize=7.5, va="top")

# ── Animated objects ──────────────────────────────────────────────────────────
FRAMES      = 160
DECAY_FRAME = 80
TRAVEL_END  = 5.0

higgs_core = Circle((0, 0), 0.22, color=HIGGS_COL, zorder=5)
ax_main.add_patch(higgs_core)

glow_rings = [Circle((0, 0), r, color=HIGGS_COL, fill=False,
                      linewidth=0.8, alpha=0.35 - i * 0.06, zorder=4)
              for i, r in enumerate([0.38, 0.55, 0.72])]
for g in glow_rings:
    ax_main.add_patch(g)

higgs_label = ax_main.text(0, 0.45, "H⁰", color="white",
                            fontsize=11, fontweight="bold",
                            ha="center", va="bottom", zorder=6)

trail_x, trail_y = [], []
trail_line, = ax_main.plot([], [], color=HIGGS_COL, linewidth=1.2,
                           alpha=0.35, zorder=3)

arrow_b    = FancyArrowPatch((0, 0), (1, 1), arrowstyle="-|>",
                              color=BQUARK, linewidth=2.5,
                              mutation_scale=14, zorder=5, visible=False)
arrow_bbar = FancyArrowPatch((0, 0), (1, -1), arrowstyle="-|>",
                              color=BBAR, linewidth=2.5,
                              mutation_scale=14, zorder=5, visible=False)
ax_main.add_patch(arrow_b)
ax_main.add_patch(arrow_bbar)

label_b    = ax_main.text(0, 0, "b  (bottom quark)", color=BQUARK,
                           fontsize=8, fontweight="bold",
                           ha="left", va="bottom", visible=False, zorder=6)
label_bbar = ax_main.text(0, 0, "b̄  (anti-bottom)", color=BBAR,
                           fontsize=8, fontweight="bold",
                           ha="left", va="top", visible=False, zorder=6)

decay_text = ax_main.text(TRAVEL_END, 0.1, "", color="white",
                           fontsize=13, fontweight="bold",
                           ha="center", va="bottom", zorder=7)

# Live caption at the bottom of the animation panel
caption = ax_main.text(5, -2.82, "", color="#aaaacc", fontsize=8,
                        ha="center", va="bottom", style="italic", zorder=7)

pulse_circles = [Circle((0, 0), 0, fill=False, color="white",
                          linewidth=1, alpha=0, zorder=4)
                 for _ in range(4)]
for pc in pulse_circles:
    ax_main.add_patch(pc)

ax_main.plot([], [], color=HIGGS_COL, linewidth=3, label="Higgs boson  H⁰")
ax_main.plot([], [], color=BQUARK,    linewidth=3, label="bottom quark  b")
ax_main.plot([], [], color=BBAR,      linewidth=3, label="anti-bottom  b̄")
ax_main.legend(fontsize=8, loc="upper left",
               facecolor="#11112a", edgecolor="#333355", labelcolor="white")

# ── Update function ───────────────────────────────────────────────────────────
def update(frame):
    if frame == 0:
        trail_x.clear()
        trail_y.clear()

    if frame <= DECAY_FRAME:
        t  = frame / DECAY_FRAME
        hx = t * TRAVEL_END
        hy = 0.18 * np.sin(6 * np.pi * t)

        higgs_core.center = (hx, hy)
        for i, g in enumerate(glow_rings):
            g.center = (hx, hy)
            g.set_alpha(0.35 - i * 0.06)
        higgs_label.set_position((hx, hy + 0.45))

        trail_x.append(hx)
        trail_y.append(hy)
        trail_line.set_data(trail_x, trail_y)

        caption.set_text("The Higgs boson travels through the Higgs field — a field that exists everywhere in space.")
        decay_text.set_text("")
        arrow_b.set_visible(False)
        arrow_bbar.set_visible(False)
        label_b.set_visible(False)
        label_bbar.set_visible(False)
        for pc in pulse_circles:
            pc.set_alpha(0)

    else:
        dt = (frame - DECAY_FRAME) / (FRAMES - DECAY_FRAME)

        higgs_core.center = (100, 100)
        for g in glow_rings:
            g.center = (100, 100)
        higgs_label.set_position((100, 100))

        if dt < 0.35:
            decay_text.set_text("DECAY!")
            decay_text.set_alpha(1 - dt / 0.35)
            caption.set_text("The Higgs boson is unstable — it breaks apart almost instantly after being created.")
        else:
            decay_text.set_text("")
            caption.set_text("It splits into a bottom quark + anti-bottom quark.  Energy becomes matter!")

        for i, pc in enumerate(pulse_circles):
            delay = i * 0.12
            if dt > delay:
                r     = (dt - delay) * 3.5
                alpha = max(0, 0.6 - (dt - delay) * 1.2)
                pc.center = (TRAVEL_END, 0)
                pc.set_radius(r)
                pc.set_alpha(alpha)

        spread = min(dt * 4, 1.0)
        bx  = TRAVEL_END + spread * 4.5
        by  =  spread * 2.2
        bx2 = TRAVEL_END + spread * 4.5
        by2 = -spread * 2.2

        arrow_b.set_positions((TRAVEL_END, 0), (bx,  by))
        arrow_bbar.set_positions((TRAVEL_END, 0), (bx2, by2))
        arrow_b.set_visible(True)
        arrow_bbar.set_visible(True)

        label_b.set_position((bx + 0.15,  by + 0.1))
        label_b.set_visible(True)
        label_bbar.set_position((bx2 + 0.15, by2 - 0.15))
        label_bbar.set_visible(True)

    return ([higgs_core, higgs_label, trail_line, decay_text, caption,
             arrow_b, arrow_bbar, label_b, label_bbar]
            + glow_rings + pulse_circles)

# ── Run ───────────────────────────────────────────────────────────────────────
ani = animation.FuncAnimation(
    fig, update,
    frames=FRAMES,
    interval=35,
    blit=False,
    repeat=True,
    repeat_delay=1500,
)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
