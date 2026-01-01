from datetime import datetime
import subprocess
import sys

def run_step(name, cmd):
    print(f"\n[{datetime.now()}] START: {name}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] {name} failed")
        sys.exit(1)
    print(f"[{datetime.now()}] DONE: {name}")

if __name__ == "__main__":
    run_step(
        "Load cleaned reviews into MySQL",
        "python load_to_mysql.py"
    )

    print("\nPipeline finished successfully.")
