# assignment3_pyramid_building_optimized.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_triangle(ax, x, y, size, upright=True, color="skyblue"):
    """Optimized triangle drawing with pre-computed height"""
    h = size * 0.866025  # Pre-computed sqrt(3)/2 ≈ 0.866025
    if upright:
        coords = [(x, y), (x + size, y), (x + size * 0.5, y + h)]
    else:
        coords = [(x, y + h), (x + size, y + h), (x + size * 0.5, y)]
    ax.add_patch(patches.Polygon(coords, closed=True, facecolor=color, edgecolor="black"))

def pyramid(depth, size=2):
    """Optimized pyramid with reduced calculations"""
    fig, ax = plt.subplots(figsize=(depth * 0.8, depth * 0.6))
    
    # Pre-compute constants
    h_step = size * 0.866025  # sqrt(3)/2 * size
    half_size = size * 0.5
    
    for row in range(depth):
        # Pre-compute row values
        row_offset = (depth - row - 1) * half_size
        y_pos = row * h_step
        upright = (row & 1) == 0  # Bitwise AND faster than modulo
        color = "skyblue" if upright else "orange"
        
        # Generate triangles for this row
        for col in range(row + 1):
            x_pos = col * size + row_offset
            draw_triangle(ax, x_pos, y_pos, size, upright, color)
    
    # Set proper limits for visualization
    total_width = depth * size
    total_height = depth * h_step
    margin = size * 0.1
    
    ax.set_xlim(-margin, total_width + margin)
    ax.set_ylim(-margin, total_height + margin)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.title(f"Pyramid of Depth {depth}")
    plt.tight_layout()
    
    # Save visualization
    plt.savefig('pyramid_visualization.png', dpi=150, bbox_inches='tight')
    
    # Save pyramid data
    import json
    total_triangles = (depth * (depth + 1)) // 2
    pyramid_data = {
        'depth': depth,
        'size': size,
        'total_triangles': total_triangles,
        'upright_triangles': sum(row + 1 for row in range(depth) if row % 2 == 0),
        'inverted_triangles': sum(row + 1 for row in range(depth) if row % 2 == 1)
    }
    
    with open('pyramid_results.json', 'w') as f:
        json.dump(pyramid_data, f, indent=2)
    
    print("Results saved to pyramid_results.json and pyramid_visualization.png")
    plt.show()

if __name__ == "__main__":
    pyramid(depth=4, size=2)