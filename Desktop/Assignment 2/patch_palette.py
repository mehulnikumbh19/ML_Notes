import nbformat as nbf

with open('IS670_Assignment2_Voting_Behavior_Final.ipynb', 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

OLD = "palette={0:'#e07070', 1:'#70a0e0'}"
NEW = "palette=['#e07070','#70a0e0']"

for cell in nb.cells:
    if cell.cell_type == 'code':
        cell.source = cell.source.replace(OLD, NEW)

with open('IS670_Assignment2_Voting_Behavior_Final.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Patched palette keys.")
