import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

R_H = 1.097e7  # Rydberg constant (m⁻¹)

series = {
    "Lyman (UV)":   (1, range(2, 7),  "ultraviolet"),
    "Balmer (Vis)": (2, range(3, 8),  "visible"),
    "Paschen (IR)": (3, range(4, 9),  "infrared"),
}

fig, ax = plt.subplots(figsize=(12, 3))
ax.set_xlim(0, 2500)
ax.set_ylim(0, 1)
ax.set_xlabel("Wavelength (nm)")
ax.set_title("Hydrogen Emission Spectrum")

colors_map = {"Lyman (UV)": "purple", "Balmer (Vis)": None, "Paschen (IR)": "red"}

# Visible spectrum background for Balmer
for wl, col in [(400,"violet"),(450,"blue"),(500,"cyan"),(550,"green"),(600,"yellow"),(650,"orange"),(700,"red")]:
    ax.axvspan(wl, wl+50, alpha=0.15, color=col)

for name, (n1, n2_range, region) in series.items():
    for n2 in n2_range:
        inv_lambda = R_H * (1/n1**2 - 1/n2**2)
        wl_nm = (1 / inv_lambda) * 1e9
        color = colors_map[name] or plt.cm.nipy_spectral((wl_nm - 380) / 400)
        ax.axvline(wl_nm, color=color, linewidth=2, alpha=0.9, label=f"{name} n={n2}→{n1}: {wl_nm:.0f}nm")

ax.legend(fontsize=7, loc="upper right")
plt.tight_layout()
plt.show()
