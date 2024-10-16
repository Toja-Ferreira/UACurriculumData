import pandas as pd
import os

def sanitize_branch_name(branch_name):
    """Replace problematic characters in branch name with underscores."""
    return branch_name.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_")

def process_branch_files(base_folder_path):
    # Loop through all department folders in the base folder
    for department in os.listdir(base_folder_path):
        department_path = os.path.join(base_folder_path, department)

        if os.path.isdir(department_path):  # Check if it's a directory
            # Loop through all Excel files in the department folder
            for filename in os.listdir(department_path):
                # Only process files that do not have 'Ramo' or 'Percurso' in their names
                if (filename.endswith('.xls') or filename.endswith('.xlsx')) and not any(x in filename for x in ['Ramo', 'Percurso']):
                    file_path = os.path.join(department_path, filename)
                    print(f"Processing file: {file_path}")

                    # Read the Excel file without a header
                    df = pd.read_excel(file_path, header=None)

                    # Initialize variables for branch processing
                    current_branch = None
                    branch_data = {}
                    has_ramos = False  # Flag to track if any Ramos or Percursos are created

                    # Iterate through the DataFrame to find branch sections
                    for index, row in df.iterrows():
                        first_cell = row[0]

                        # Check if the row contains the "Ramo" or "Percurso" identifier
                        if isinstance(first_cell, str) and ("Ramo" in first_cell or "Percurso" in first_cell):
                            current_branch = first_cell.strip()

                            # Extract parts of the branch name to avoid overwriting
                            branch_name_parts = current_branch.split('-')
                            branch_name = '_'.join(part.strip() for part in branch_name_parts[1:])  # Use more parts of the name
                            branch_name = sanitize_branch_name(branch_name)  # Sanitize the branch name
                            branch_data[branch_name] = []
                            has_ramos = True


                        # If we're in a branch section, add the row data to that branch
                        elif current_branch is not None:
                            # Add only relevant discipline data (ignoring empty rows)
                            if not row.isnull().all():
                                row = row.tolist()  # Convert the row to a list
                                branch_data[branch_name].append(row)

                    # Create new Excel files for each branch
                    for branch, rows in branch_data.items():
                        if rows:
                            # Create DataFrame from rows
                            branch_df = pd.DataFrame(rows)

                            # Create new filename
                            new_file_name = f"{os.path.splitext(file_path)[0]}_Ramo_{branch}.xlsx"

                            # Write to Excel without header
                            branch_df.to_excel(new_file_name, index=False, header=False)
                            print(f"Created file: {new_file_name}")

                    # If Ramos or Percursos were found, delete the original file
                    if has_ramos:
                        os.remove(file_path)  # Delete the original file
                        print(f"Deleted original file: {file_path}")

if __name__ == "__main__":
    base_folder_path = 'data/MSC'
    process_branch_files(base_folder_path)
