import subprocess
import sys
import time

def run_step(step_name, command):
    print("\n" + "="*80)
    print(f"Executing Step: {step_name}")
    print(f"Command: {' '.join(command)}")
    print("="*80)
    start_time = time.time()
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            sys.stdout.write(line)
        process.wait()
        elapsed = time.time() - start_time
        if process.returncode == 0:
            print(f"\n[SUCCESS] Step '{step_name}' completed in {elapsed:.2f}s.")
            return True
        else:
            print(f"\n[FAILED] Step '{step_name}' failed with exit code {process.returncode} in {elapsed:.2f}s.")
            return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n[ERROR] Exception occurred running '{step_name}': {e} in {elapsed:.2f}s.")
        return False

def main():
    steps = [
        ("1. Live NAV Fetching", [sys.executable, "live_nav_fetch.py"]),
        ("2. Data Ingestion & Quality Analysis", [sys.executable, "data_ingestion.py"]),
        ("3. Pre-processing & Boundary Clipping", [sys.executable, "clean_new_datasets.py"]),
        ("4. SQLite Star Schema Load", [sys.executable, "sql_database_setup.py"]),
        ("5. Portfolio Analytics & Reporting", [sys.executable, "generate_analytics.py"]),
        ("6. Dashboard JSON Data Export", [sys.executable, "dashboard/export_dashboard_data.py"])
    ]
    
    print("*"*80)
    print("MUTUAL FUND PORTFOLIO ETL PIPELINE ORCHESTRATOR")
    print("Starting execution of all pipeline stages...")
    print("*"*80)
    
    pipeline_start = time.time()
    success_stages = []
    failed_stages = []
    
    for name, cmd in steps:
        if run_step(name, cmd):
            success_stages.append(name)
        else:
            failed_stages.append(name)
            print(f"\n[CRITICAL ERROR] Pipeline execution stopped due to failure at stage: {name}")
            break
            
    print("\n" + "*"*80)
    print("PIPELINE EXECUTION SUMMARY")
    print("*"*80)
    print(f"Total time elapsed: {time.time() - pipeline_start:.2f}s")
    print(f"Successfully completed stages ({len(success_stages)}):")
    for s in success_stages:
        print(f"  - [x] {s}")
    if failed_stages:
        print(f"Failed stages ({len(failed_stages)}):")
        for s in failed_stages:
            print(f"  - [ ] {s}")
        sys.exit(1)
    else:
        print("  - [x] All pipeline stages executed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
