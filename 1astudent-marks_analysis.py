# assignment1a_student_marks_optimized.py
import pandas as pd
import numpy as np

# Step 1: Load Data
data = {
    "StudentID": [101, 102, 103, 104, 105, 106, 107],
    "Name": ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace"],
    "Math": [95, 72, 88, 55, 80, 99, 68],
    "Physics": [89, 65, 91, 62, 77, 95, 72],
    "Chemistry": [92, 70, 85, 58, 79, 97, 74],
    "Biology": [88, 60, 90, 61, 83, 96, 70]
}
df = pd.DataFrame(data)

# Step 2: Vectorized Computations (optimized)
subject_cols = ["Math", "Physics", "Chemistry", "Biology"]
df["Total"] = df[subject_cols].sum(axis=1)
df["Average"] = df["Total"] * 0.25  # More efficient than division
df["Grade"] = pd.cut(df["Average"], bins=[0, 60, 75, 90, 100],
                     labels=["F", "C", "B", "A"], right=False)

# Step 3: Top Performers per Subject (optimized)
top_performers = {subject: df.nlargest(3, subject)[["Name", subject]] 
                 for subject in subject_cols}

# Step 4: Visualization (optimized)
avg_per_subject = df[subject_cols].mean()
plot = avg_per_subject.plot(kind="bar", title="Average Marks per Subject", 
                           ylabel="Average Marks", figsize=(8, 5))
plot.get_figure().savefig("subject_averages.png", bbox_inches='tight', dpi=150)

# Step 5: Save Results to Excel (optimized)
summary_df = df[["StudentID", "Name", "Total", "Average", "Grade"]]
top_performers_df = pd.concat(top_performers)

with pd.ExcelWriter("results.xlsx", engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
    top_performers_df.to_excel(writer, sheet_name="Top Performers")

print("Results saved to results.xlsx and subject_averages.png")