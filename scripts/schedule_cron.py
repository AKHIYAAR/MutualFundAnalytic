import os
import sys
import subprocess
import platform

def schedule_task():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    script_path = os.path.join(base_dir, 'scripts', 'etl_pipeline.py')
    python_exe = sys.executable
    
    current_os = platform.system().lower()
    
    print("ETL Ingestion Task Scheduler (Bonus B1)")
    print("=======================================")
    print(f"Target Script: {script_path}")
    print(f"Python Executable: {python_exe}")
    print(f"Detected OS: {current_os.upper()}\n")
    
    if 'windows' in current_os:
        # Windows schtasks command: Run weekly on weekdays at 8 PM (20:00)
        task_name = "Bluestocks_MF_ETL_Weekday"
        command = [
            "schtasks", "/create",
            "/tn", task_name,
            "/tr", f'"{python_exe}" "{script_path}"',
            "/sc", "weekly",
            "/d", "MON,TUE,WED,THU,FRI",
            "/st", "20:00",
            "/f" # force overwrite if exists
        ]
        
        print("Executing scheduled task creation on Windows:")
        print(" ".join(command))
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("\n[SUCCESS] Windows Task Scheduler successfully configured.")
            print(result.stdout)
        except Exception as e:
            print(f"\n[WARNING] Could not register scheduled task: {e}")
            print("Please run this command in an elevated Administrator prompt to create the task:")
            print(f'schtasks /create /tn "{task_name}" /tr "\\"{python_exe}\\" \\"{script_path}\\"" /sc weekly /d MON,TUE,WED,THU,FRI /st 20:00')
            
    else:
        # Linux/macOS Cron definition: 0 20 * * 1-5 (8 PM, Mon-Fri)
        cron_entry = f"0 20 * * 1-5 {python_exe} {script_path} >> {os.path.join(base_dir, 'reports', 'cron_etl.log')} 2>&1"
        print("For Unix-based platforms (Linux/macOS), add this line to your crontab (crontab -e):")
        print("-" * 80)
        print(cron_entry)
        print("-" * 80)
        
        # Optionally write to a local script to make it easy
        cron_sh = os.path.join(base_dir, 'scripts', 'setup_cron.sh')
        with open(cron_sh, 'w') as f:
            f.write(f"#(crontab -l 2>/dev/null; echo \"{cron_entry}\") | crontab -\n")
        print(f"Helper shell script written to: {cron_sh}")

if __name__ == '__main__':
    schedule_task()
