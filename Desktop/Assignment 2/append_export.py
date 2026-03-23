import nbformat as nbf

with open('IS670_Assignment2_Voting_Behavior_Final.ipynb', 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

export_code = """# =========================================================================
# Run this cell LAST to export the notebook to a standalone HTML file.
# IMPORTANT: Before running this, click "File -> Save" at the top of Colab
# so the latest outputs are written to Drive.
# =========================================================================

notebook_path = "/content/drive/MyDrive/IS 670/IS670_Assignment2_Voting_Behavior_Final.ipynb"
!jupyter nbconvert --to html "{notebook_path}"
"""

# Append the HTML conversion cell if it isn't already there
if not any("jupyter nbconvert" in c.source for c in nb.cells):
    nb.cells.append(nbf.v4.new_markdown_cell("## 8. Export to HTML"))
    nb.cells.append(nbf.v4.new_code_cell(export_code))
    
    with open('IS670_Assignment2_Voting_Behavior_Final.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Export code cell appended to notebook.")
else:
    print("Notebook already contains export cell.")
