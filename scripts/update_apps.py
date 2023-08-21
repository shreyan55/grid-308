import os
import sys
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent
app_name = sys.argv[1]
file_path = file_path / f"apps/{app_name}/apps.py"
print(file_path)
if app_name:
    apps_py_path = file_path
    with open(apps_py_path, "r") as f:
        content = f.read()

    updated_content = content.replace(f'name = "{app_name}"', f'name = "apps.{app_name}"')
    updated_content = content.replace(f"name = '{app_name}'", f"name = 'apps.{app_name}'")

    with open(apps_py_path, "w") as f:
        f.write(updated_content)
