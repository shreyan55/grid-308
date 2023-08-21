import ast
import sys
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent
file_path = file_path / "config/settings/local_apps.py"


new_string = sys.argv[1]

with open(file_path, 'r') as file:
    file_contents = file.read()

ast_tree = ast.parse(file_contents)

for node in ast_tree.body:
    if isinstance(node, ast.Assign) and node.targets[0].id == 'LOCAL_APPS':
        list_node = node.value
        list_node.elts.append(ast.Str(s=new_string))

updated_code = ast.unparse(ast_tree)

with open(file_path, 'w') as file:
    file.write(updated_code)
