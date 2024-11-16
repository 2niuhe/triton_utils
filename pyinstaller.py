import subprocess

# import nicegui

cmd = [
    "python",
    "-m",
    "PyInstaller",
    "main.py",
    "--name",
    "add_by_three",
    "--onefile",
    # "--add-data", f"{Path(nicegui.__file__).parent}{os.pathsep}nicegui",
    "--exclude-module",
    "ruff",
]
subprocess.call(cmd)
