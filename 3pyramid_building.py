import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json

def draw_triangle(ax, x, y, size, upright=True, color="skyblue"):
    """Draw a triangle with proper coordinates"""
    h = size * 0.866025  # Height of equilateral triangle
    if upright:
        # Upright triangle: base at bottom, apex at top
        coords = [(x, y), (x + size, y), (x + size/2, y + h)]
    else:
        # Inverted triangle: base at top, apex at bottom
        coords = [(x, y + h), (x + size, y + h), (x + size/2, y)]
    ax.add_patch(patches.Polygon(coords, closed=True, facecolor=color, edgecolor="black", linewidth=0.5))

def pyramid(depth, size=2):
    """Create a properly tessellated pyramid"""
    fig, ax = plt.subplots(figsize=(depth * 1.2, depth * 0.8))
    
    h = size * 0.866025  # Triangle height
    upright_count = 0
    inverted_count = 0
    
    # Calculate total pyramid width for centering
    max_width = depth * size
    
    # Draw all upright triangles first
    for row in range(depth):
        # Y position: start from top, go down
        y = (depth - row - 1) * h
        
        # Number of triangles in this row
        triangles_in_row = row + 1
        
        # X offset to center this row
        row_width = triangles_in_row * size
        x_start = (max_width - row_width) / 2
        
        # Draw upright triangles for this row
        for col in range(triangles_in_row):
            x = x_start + col * size
            draw_triangle(ax, x, y, size, upright=True, color="skyblue")
            upright_count += 1
    
    
    for row in range(depth - 1):  
        # Y positions
        upper_y = (depth - row - 1) * h      # Upper row Y
        lower_y = (depth - row - 2) * h      # Lower row Y
        
        
        inv_y = lower_y  # Base of inverted triangle at lower row level
        
        # Calculate X positions based on the lower row
        lower_triangles = row + 2
        lower_row_width = lower_triangles * size
        lower_x_start = (max_width - lower_row_width) / 2
        
       
        for col in range(row + 1):
            # Position inverted triangle in the gap between lower row triangles
            inv_x = lower_x_start + size * (col + 0.5)
            draw_triangle(ax, inv_x, inv_y, size, upright=False, color="orange")
            inverted_count += 1
    
    total_triangles = upright_count + inverted_count
    
    # Set visualization limits
    margin = size * 0.3
    ax.set_xlim(-margin, max_width + margin)
    ax.set_ylim(-margin, depth * h + margin)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.title(f"Tessellated Pyramid - Depth {depth}")
    plt.tight_layout()
    
    # Save pyramid data
    pyramid_data = {
        'depth': depth,
        'size': size,
        'total_triangles': total_triangles,
        'upright_triangles': upright_count,
        'inverted_triangles': inverted_count
    }
    
    with open('pyramid_results.json', 'w') as f:
        json.dump(pyramid_data, f, indent=2)
    
    # Save visualization
    plt.savefig('pyramid_visualization.png', dpi=150, bbox_inches='tight')
    
    print(f"Pyramid (depth {depth}) created with {total_triangles} triangles:")
    print(f"  - {upright_count} upright triangles (skyblue)")
    print(f"  - {inverted_count} inverted triangles (orange)")
    print("Results saved to pyramid_results.json and pyramid_visualization.png")
    
    plt.show()

if __name__ == "__main__":
    pyramid(depth=4, size=2)