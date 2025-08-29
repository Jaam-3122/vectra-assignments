# assignment-1b_polygon_geometry.py
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

points = np.array([
    (9.05, 7.76),
    (12.5, 3.0),
    (10.0, 0.0),
    (5.0, 0.0),
    (2.5, 3.0)
])

# Create polygon once
poly = Polygon(points)

# Pre-compute rolled arrays 
points_rolled = np.roll(points, -1, axis=0)
x, y = points[:, 0], points[:, 1]
x_rolled, y_rolled = points_rolled[:, 0], points_rolled[:, 1]

# Edge vectors and lengths (vectorized)
edges = points_rolled - points
lengths = np.linalg.norm(edges, axis=1)

# Area using shoelace formula
area_shoelace = 0.5 * np.abs(np.sum(x * y_rolled - y * x_rolled))

# Interior angles
n_points = len(points)
v1 = np.roll(points, 1, axis=0) - points  # Previous vertex vectors
v2 = points_rolled - points                # Next vertex vectors

# Vectorized dot products and norms
dot_products = np.sum(v1 * v2, axis=1)
norms_v1 = np.linalg.norm(v1, axis=1)
norms_v2 = np.linalg.norm(v2, axis=1)


cos_angles = np.clip(dot_products / (norms_v1 * norms_v2), -1, 1)
angles = np.degrees(np.arccos(cos_angles))

is_convex = np.all(angles < 180)

# Centroid
centroid = points.mean(axis=0)

#results
print(f"Polygon Area: {area_shoelace:.6f} | Shapely Area: {poly.area:.6f}")
print(f"Edge Lengths: {lengths}")
print(f"Interior Angles: {angles}")
print(f"Is Convex: {is_convex}")
print(f"Centroid: {centroid} | Shapely Centroid: ({poly.centroid.x:.6f}, {poly.centroid.y:.6f})")

# Saving to file
results = {
    'polygon_area_shoelace': area_shoelace,
    'polygon_area_shapely': poly.area,
    'edge_lengths': lengths.tolist(),
    'interior_angles': angles.tolist(),
    'is_convex': bool(is_convex),
    'centroid_calculated': centroid.tolist(),
    'centroid_shapely': [poly.centroid.x, poly.centroid.y]
}

import json
with open('polygon_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Save plot
plt.savefig('polygon_visualization.png', dpi=150, bbox_inches='tight')
print("Results saved to polygon_results.json and polygon_visualization.png")

# Visualization
fig, ax = plt.subplots(figsize=(8, 6))
ax.fill(x, y, alpha=0.3, edgecolor="black", linewidth=2)


for i, (px, py) in enumerate(points):
    ax.text(px, py, f"V{i+1}", fontsize=10, ha='center', va='center')

ax.scatter(*centroid, color="red", s=50, label="Centroid", zorder=5)
ax.legend()
ax.set_title("Polygon with Vertices and Centroid")
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')
plt.tight_layout()
plt.show()