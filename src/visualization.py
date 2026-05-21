# =========================================================
# INTERACTIVE DASHBOARD - POPULATION VISUALIZATION
# =========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_excel("data/updated_population_data.xlsx")

# Create sample Age column if not present
if 'Age' not in df.columns:
    np.random.seed(42)
    df['Age'] = np.random.randint(18, 60, size=len(df))

# =========================================================
# CREATE MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Population Visualization Dashboard")
root.geometry("1400x700")
root.configure(bg="#f4f4f4")

# =========================================================
# HEADER
# =========================================================

title = tk.Label(
    root,
    text="Population Visualization Dashboard",
    font=("Arial", 24, "bold"),
    bg="#4a90e2",
    fg="white",
    pady=15
)

title.pack(fill="x")

# =========================================================
# FILTER FRAME
# =========================================================

filter_frame = tk.Frame(root, bg="#f4f4f4")
filter_frame.pack(pady=10)

tk.Label(
    filter_frame,
    text="Select Gender:",
    font=("Arial", 12, "bold"),
    bg="#f4f4f4"
).grid(row=0, column=0, padx=10)

gender_var = tk.StringVar()
gender_dropdown = ttk.Combobox(
    filter_frame,
    textvariable=gender_var,
    values=["All", "Male", "Female"],
    state="readonly",
    width=15
)

gender_dropdown.current(0)
gender_dropdown.grid(row=0, column=1, padx=10)

# =========================================================
# CHART FRAME
# =========================================================

chart_frame = tk.Frame(root, bg="white")
chart_frame.pack(fill="both", expand=True, padx=20, pady=20)

# =========================================================
# FUNCTION TO UPDATE CHARTS
# =========================================================

def update_charts():

    for widget in chart_frame.winfo_children():
        widget.destroy()

    selected_gender = gender_var.get()

    # Filter data
    if selected_gender == "All":
        filtered_df = df
    else:
        filtered_df = df[df['Gender'] == selected_gender]

    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # =====================================================
    # BAR CHART
    # =====================================================

    gender_counts = filtered_df['Gender'].value_counts()

    sns.barplot(
        x=gender_counts.index,
        y=gender_counts.values,
        ax=axes[0]
    )

    axes[0].set_title("Gender Distribution")
    axes[0].set_xlabel("Gender")
    axes[0].set_ylabel("Count")

    # Add labels
    for i, value in enumerate(gender_counts.values):
        axes[0].text(i, value + 1, str(value), ha='center')

    # =====================================================
    # HISTOGRAM
    # =====================================================

    sns.histplot(
        filtered_df['Age'],
        bins=8,
        kde=True,
        ax=axes[1]
    )

    axes[1].set_title("Age Distribution")
    axes[1].set_xlabel("Age")
    axes[1].set_ylabel("Frequency")

    # =====================================================
    # DISPLAY CHARTS
    # =====================================================

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# =========================================================
# BUTTON
# =========================================================

update_button = tk.Button(
    filter_frame,
    text="Update Dashboard",
    font=("Arial", 12, "bold"),
    bg="#4a90e2",
    fg="white",
    padx=20,
    pady=5,
    command=update_charts
)

update_button.grid(row=0, column=2, padx=20)

# =========================================================
# INITIAL CHART LOAD
# =========================================================

update_charts()

# =========================================================
# RUN APPLICATION
# =========================================================

root.mainloop()