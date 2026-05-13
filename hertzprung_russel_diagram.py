import numpy as np
import matplotlib.pyplot as plt

# 1. Structured stellar catalog data
star_data = [
    {"name": "Sun", "temp": 5778, "lum": 1.0, "type": "Main Sequence"},
    {"name": "Sirius A", "temp": 9940, "lum": 25.4, "type": "Main Sequence"},
    {"name": "Betelgeuse", "temp": 3500, "lum": 126000.0, "type": "Supergiant"},
    {"name": "Rigel", "temp": 12100, "lum": 120000.0, "type": "Supergiant"},
    {"name": "Aldebaran", "temp": 3910, "lum": 518.0, "type": "Red Giant"},
    {"name": "Arcturus", "temp": 4286, "lum": 170.0, "type": "Red Giant"},
    {"name": "Proxima Centauri", "temp": 3042, "lum": 0.0017, "type": "Main Sequence (Red Dwarf)"},
    {"name": "Sirius B", "temp": 25200, "lum": 0.026, "type": "White Dwarf"},
    {"name": "Procyon B", "temp": 7740, "lum": 0.00055, "type": "White Dwarf"},
    {"name": "Vega", "temp": 9600, "lum": 40.1, "type": "Main Sequence"}
]

# Extract plotting coordinate vectors
temps = np.array([s["temp"] for s in star_data])
lums = np.array([s["lum"] for s in star_data])

# 2. Configure plotting frame and canvas aesthetics
fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor('#0b0c10') 
ax.set_facecolor('#1f2833')

# Map temperature values to realistic stellar colors using a sequential colormap
scatter = ax.scatter(temps, lums, c=temps, cmap='RdYlBu', s=150, edgecolors='white', picker=True, zorder=3)

# 3. Apply canonical astrophysics formatting rules
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(30000, 2000) # CRITICAL: H-R diagram temperature x-axis is inverted
ax.set_ylim(1e-5, 1e6)

# Labels & grid lines
ax.set_title("Interactive Hertzsprung-Russell Diagram", fontsize=14, color='white', pad=15)
ax.set_xlabel("Effective Temperature (Kelvin)", fontsize=11, color='white')
ax.set_ylabel("Luminosity (Relative to the Sun)", fontsize=11, color='white')
ax.tick_params(colors='white', which='both')
ax.grid(True, which="both", ls="--", color='#45a29e', alpha=0.3)

# 4. Generate a persistent information box overlay text object
info_text = ax.text(0.05, 0.05, "Click a star to inspect properties.", 
                    transform=ax.transAxes, color='#66fcf1', fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b0c10', edgecolor='#66fcf1', alpha=0.85))

# 5. Handle user selection event logic
def on_pick(event):
    # Retrieve the internal array element index of the clicked marker
    index = event.ind[0]
    star = star_data[index]
    
    # Format and inject properties into the canvas box layout
    details = (f"★ {star['name']} ★\n"
               f"Classification: {star['type']}\n"
               f"Temperature: {star['temp']:,} K\n"
               f"Luminosity: {star['lum']:,} L☉")
    
    info_text.set_text(details)
    fig.canvas.draw_idle() # Prompt canvas render loop to cleanly redraw text

# Connect pick event listener directly to window object
fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()
