import os
import sys

# Template for per-project README
README_TEMPLATE = """# {project_name}

## 📌 Project Overview
Brief description of the project (problem statement, business context).

## 📊 Dataset
- Source: 
- Size/Features: 
- Notes: 

## ⚙️ Methods
- Data preprocessing
- Feature engineering
- Model(s) used
- Evaluation metrics

## 📈 Results
- Key findings
- Business insights
- Visualizations

## 🚀 Next Steps
- Improvements
- Possible extensions
"""

# Template for requirements.txt
REQUIREMENTS_TEMPLATE = """# Add your project dependencies here
# Example:
# pandas
# scikit-learn
# matplotlib
"""

def create_project_structure(project_name):
    # Define folder structure
    folders = [
        f"{project_name}/data",
        f"{project_name}/notebooks",
        f"{project_name}/src",
        f"{project_name}/reports",
    ]

    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Create README.md
    readme_path = os.path.join(project_name, "README.md")
    with open(readme_path, "w") as f:
        f.write(README_TEMPLATE.format(project_name=project_name))

    # Create requirements.txt
    req_path = os.path.join(project_name, "requirements.txt")
    with open(req_path, "w") as f:
        f.write(REQUIREMENTS_TEMPLATE)

    print(f"✅ Project '{project_name}' created successfully!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_project.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    create_project_structure(project_name)
