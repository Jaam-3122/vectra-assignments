# assignment2_room_tiling_optimized.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def tile_room(m, n):
    """Optimized room tiling with grid tracking"""
    tiles = [(4, "green"), (3, "yellow"), (2, "blue"), (1, "red")]
    room = []
    grid = np.zeros((n, m), dtype=bool)  # Track filled spaces efficiently
    
    for size, color in tiles:
        for y in range(0, n - size + 1, size):  # Step by tile size
            for x in range(0, m - size + 1, size):
                if not grid[y:y+size, x:x+size].any():  # Vectorized check
                    room.append((x, y, size, color))
                    grid[y:y+size, x:x+size] = True
    
    return room

def visualize(m, n, tiles):
    """Optimized visualization"""
    fig, ax = plt.subplots(figsize=(m*0.6, n*0.6))
    
    for x, y, size, color in tiles:
        ax.add_patch(patches.Rectangle((x, y), size, size, 
                                     facecolor=color, edgecolor="black"))
    
    ax.set_xlim(0, m)
    ax.set_ylim(0, n)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    plt.title(f"Tiling {m}×{n} Room")
    plt.tight_layout()

    # Save visualization
    plt.savefig('room_tiling.png', dpi=150, bbox_inches='tight')

# Save tiling data
    import json
    tiling_data = {
        'room_dimensions': [m, n],
        'tiles': [{'x': x, 'y': y, 'size': size, 'color': color} 
            for x, y, size, color in tiles],
        'total_tiles': len(tiles),
        'coverage_area': sum(size*size for _, _, size, _ in tiles)
    }

    with open('tiling_results.json', 'w') as f:
        json.dump(tiling_data, f, indent=2)

    plt.show()

if __name__ == "__main__":
    m, n = 10, 8
    tiles = tile_room(m, n)
    visualize(m, n, tiles)
    print("Results saved to tiling_results.json and room_tiling.png")