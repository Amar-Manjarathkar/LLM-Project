import os
from pathlib import Path

def create_project_structure():
    # 1. Define the Project Name
    project_name = "UPEF_Project"
    
    # 2. Define the Folder Hierarchy
    structure = {
        project_name: [
            "src",                 # Main source code
            "src/cleaning",        # Your data cleaning logic (Step 0)
            "src/models",          # Ollama/Model interaction logic
            "src/pipeline",        # Orchestration logic
            "data",                # Data storage
            "data/raw",            # Raw input dump
            "data/processed",      # Cleaned JSON ready for analysis
            "prompts",             # Store your System Prompts/CoT templates
            "config",              # Configuration files (YAML/JSON)
            "tests",               # Unit tests for the pipeline
            "notebooks",           # Jupyter notebooks for experiments
        ]
    }

    # 3. Define Key Files to Create (Empty for now)
    files = {
        f"{project_name}/README.md": "# Unified Prompt Engineering Framework (UPEF)\n\nProject for Language ID, Domain Classification, and NER using Local LLMs.",
        f"{project_name}/requirements.txt": "", # We will fill this in the next step
        f"{project_name}/.env": "# Environment Variables (API Keys, Model Names)",
        f"{project_name}/.gitignore": "venv/\n__pycache__/\n*.env\n.DS_Store\n/data/*\n!/data/.gitkeep",
        f"{project_name}/src/__init__.py": "",
        f"{project_name}/src/cleaning/__init__.py": "",
        f"{project_name}/src/models/__init__.py": "",
        f"{project_name}/src/pipeline/__init__.py": "",
        f"{project_name}/main.py": "# Entry point for the pipeline"
    }

    print(f"🚀 Initializing {project_name} structure...")

    # 4. Create Directories
    for root, folders in structure.items():
        # Create root
        Path(root).mkdir(exist_ok=True)
        # Create subfolders
        for folder in folders:
            path = Path(root) / folder
            path.mkdir(parents=True, exist_ok=True)
            # Add .gitkeep to ensure empty folders are tracked if using git
            (path / ".gitkeep").touch()
            print(f"   [DIR]  Created: {path}")

    # 5. Create Files
    for file_path, content in files.items():
        path = Path(file_path)
        if not path.exists():
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   [FILE] Created: {path}")
        else:
            print(f"   [SKIP] Exists:  {path}")

    print("\n✅ Mission Complete. Project structure ready.")
    print(f"📂 Go into your directory: cd {project_name}")

if __name__ == "__main__":
    create_project_structure()