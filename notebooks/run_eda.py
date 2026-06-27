import os
import subprocess
import sys

def main():
    # Find the notebooks directory and switch to it to ensure relative paths resolve correctly
    notebooks_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(notebooks_dir)
    print(f"Working directory changed to: {os.getcwd()}")
    
    # 1. Run build_eda_notebook.py to generate the template notebook
    print("Regenerating the notebook template...")
    subprocess.run([sys.executable, "build_eda_notebook.py"], check=True)
    
    # 2. Execute the notebook in-place using jupyter nbconvert
    print("Executing the notebook cells and saving outputs...")
    cmd = [
        "jupyter", "nbconvert", 
        "--to", "notebook", 
        "--execute", 
        "--inplace", 
        "EDA_Analysis.ipynb"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print("[SUCCESS] Notebook successfully executed and saved in-place.")

if __name__ == "__main__":
    main()
