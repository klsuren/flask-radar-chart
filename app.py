from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import os

app = Flask(__name__)

# Define skills for radar chart
SKILLS = ["Python", "SQL", "Tableau", "Machine Learning", "AI", "Excel", "Power BI", "AWS", "Deep Learning"]

import plotly.graph_objects as go

import plotly.graph_objects as go

# Define required skills
SKILLS = ["Python", "Sql", "Tableau", "Machine learning", "AI", "Excel", "Power Bi", "AWS", "Deep Learning"]

def generate_radar_chart(emp_id):
    # Read Excel file
    xls = pd.ExcelFile("sampledata.xlsx")

    try:
        manager_df = pd.read_excel(xls, "manager_validated")
        required_df = pd.read_excel(xls, "required_ratings")
    except ValueError:
        return None, "Error: Sheet names incorrect"

    # Standardize column names (strip spaces)
    manager_df.columns = manager_df.columns.str.strip()
    required_df.columns = required_df.columns.str.strip()

    # Check if Employee ID exists
    if emp_id not in manager_df["Employee ID"].values:
        return None, "Employee ID not found"

    # Get employee data
    manager_data = manager_df[manager_df["Employee ID"] == emp_id]
    employee_name = manager_data["Name"].values[0] if "Name" in manager_data.columns else "Unknown"

    # Extract ratings for required skills
    manager_ratings = [manager_data.get(skill, 0).values[0] if skill in manager_data.columns else 0 for skill in SKILLS]
    required_ratings = [required_df.get(skill, 0).values[0] if skill in required_df.columns else 0 for skill in SKILLS]

    # Ensure the first and last points are the same to close the chart
    manager_ratings.append(manager_ratings[0])
    required_ratings.append(required_ratings[0])
    skills_labels = SKILLS + [SKILLS[0]]  # Closing the loop

    # Create Radar Chart with Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=manager_ratings,
        theta=skills_labels,
        fill='toself',
        name='Manager Ratings',
        marker=dict(color='#1E88E5', opacity=0.8),  # **Deep Blue**
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatterpolar(
        r=required_ratings,
        theta=skills_labels,
        fill='toself',
        name='Required Ratings',
        marker=dict(color='#43A047', opacity=0.7),  # **Vibrant Green**
        line=dict(width=3, dash="dot")  # Dotted line for better distinction
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], showgrid=True, gridcolor="lightgray"),
        ),
        showlegend=True,
        title=f"Skill Ratings for {employee_name}",
        template="plotly_white"  # Clean white background
    )

    # Save the chart as an HTML file
    chart_path = "static/radar_chart.html"
    fig.write_html(chart_path)

    return chart_path, employee_name



@app.route("/", methods=["GET", "POST"])
def index():
    chart_path = None
    employee_name = None
    error_message = None

    if request.method == "POST":
        emp_id = request.form.get("emp_id")
        if emp_id:
            try:
                emp_id = int(emp_id)  # Convert ID to integer
                chart_path, employee_name = generate_radar_chart(emp_id)
                if not chart_path:
                    error_message = employee_name  # If error occurs, store message
            except ValueError:
                error_message = "Invalid Employee ID format"

    return render_template("index.html", chart_path=chart_path, employee_name=employee_name, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)



