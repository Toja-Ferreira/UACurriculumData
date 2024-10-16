import pandas as pd
import os


def load_master_curricular_plans(base_folder_path):
    # List to hold DataFrames
    dataframes = []

    # Loop through all department folders in the base folder
    for department in os.listdir(base_folder_path):
        department_path = os.path.join(base_folder_path, department)

        if os.path.isdir(department_path):  # Check if it's a directory
            # Loop through all Excel files in the department folder
            for filename in os.listdir(department_path):
                if filename.endswith('.xls') or filename.endswith('.xlsx'):
                    file_path = os.path.join(department_path, filename)
                    print(f"Loading file: {file_path}")

                    # Read the Excel file
                    df = pd.read_excel(file_path)

                    # Convert the 'NOMEDISCIPLINAGENERICA' column to strings and filter out rows where it contains "OPÇÃO LIVRE"
                    df['NOMEDISCIPLINAGENERICA'] = df['NOMEDISCIPLINAGENERICA'].astype(str)
                    df = df[~df['NOMEDISCIPLINAGENERICA'].str.contains("OPÇÃO LIVRE", case=False, na=False)]

                    # Add columns for department, MSC, and Ramo/Percurso name
                    msc_value = filename[11:-5]  # Get the full filename without extension

                    # Initialize ramo_value as None by default
                    ramo_value = None

                    # Extract the Ramo or Percurso portion (assuming either "Ramo" or "Percurso" exists in the filename)
                    if 'Ramo' in msc_value:  # Check if "Ramo" is part of the filename
                        ramo_value = msc_value.split('Ramo')[-1].strip()  # Take the part after "Ramo"
                        ramo_value = ramo_value.lstrip('_')  # Remove leading underscore from Ramo value
                        msc_value = msc_value.split('Ramo')[0].strip().rstrip('_')  # Take the part before "Ramo" and remove trailing underscore
                    elif 'Percurso' in msc_value:  # Check if "Percurso" is part of the filename
                        percurso_value = msc_value.split('Percurso')[-1].strip()  # Take the part after "Percurso"
                        percurso_value = percurso_value.lstrip('_')  # Remove leading underscore from Percurso value
                        ramo_value = f"Percurso_{percurso_value}"  # Combine into Percurso_x format
                        msc_value = msc_value.split('Percurso')[0].strip().rstrip('_')  # Take the part before "Percurso" and remove trailing underscore
                    else:
                        ramo_value = None  # Handle cases where there's no "Ramo" or "Percurso"

                    # Assign values to the DataFrame
                    df['DEPARTMENT'] = department
                    df['MSC'] = msc_value  # Assign the cleaned MSC value
                    df['RAMO'] = ramo_value  # Add the Ramo or Percurso value


                    # Move the columns "Department" and "MSC" to the third and fourth positions
                    cols = df.columns.tolist()
                    if 'NOMEDISCIPLINA' in cols and 'CODDISCIPLINA' in cols:
                        cols = cols[:2] + [cols[-2]] + [cols[-1]] + cols[2:-2]
                        df = df[cols]

                    # Append the DataFrame to the list
                    dataframes.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df

def load_ce_files(folder_path):
    # List to hold DataFrames
    dataframes = []

    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.xls') or filename.endswith('.xlsx'):
            file_path = os.path.join(folder_path, filename)
            print(f"Loading file: {file_path}")

            # Read the Excel file
            df = pd.read_excel(file_path)

            # Remove the file extension
            filename = os.path.splitext(filename)[0]

            # Extract the departments and course code from the filename
            parts = filename.split('_')
            departments = parts[:-3]
            course = '_'.join(parts[-2:])

            # Iterate over each department and create a copy of the DataFrame for each
            for department in departments:
                # Create a copy of the DataFrame for the current department
                df_copy = df.copy()
                
                # Add the 'DEPARTMENT' column
                df_copy['DEPARTMENT'] = department
                
                # Add a column for the course (CE)
                df_copy['CE'] = course
                
                # Move the "CE" column to the third position, after "NOMEDISCIPLINA" and "CODDISCIPLINA"
                cols = df_copy.columns.tolist()
                if len(cols) > 2:  # Ensure there are enough columns to rearrange
                    cols = cols[:2] + [cols[-1]] + cols[2:-1]  # Adjust position of 'CE' column
                    df_copy = df_copy[cols]

                # Append the modified DataFrame to the list
                dataframes.append(df_copy)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df

def load_microcredentials(file_path):
    # Load the microcredential data from the specified file
    df = pd.read_excel(file_path)  # Use pd.read_csv(file_path) if the file is a CSV

    # Display the original DataFrame
    print("Original DataFrame:")
    print(df.head())

    # Add a new column 'NOMEDISCIPLINA' that is the same as the new 'Microcredencial'
    df['NOMEDISCIPLINA'] = df['Microcredencial']

    # Create the 'NOMEDISCIPLINA' column by concatenating 'CODIGOMICROCREDENCIAL' and 'NOMEDISCIPLINA'
    df['Microcredencial'] = df.apply(lambda x: f"{x['CODIGOMICROCREDENCIAL']}_{x['Microcredencial']}", axis=1)

    # Drop the original 'CODIGOMICROCREDENCIAL' column if it's no longer needed
    df.drop(columns=['CODIGOMICROCREDENCIAL'], inplace=True)

    # Normalize the department column to lowercase
    if 'Department' in df.columns:
        df['Department'] = df['Department'].str.lower()
        df.rename(columns={'Department': 'DEPARTMENT'}, inplace=True)

    # The order of the columns should be the current positions: 3, 2, 4, 0, 1
    cols = df.columns.tolist()
    cols = cols[2:3] + cols[4:5] + cols[3:4] + cols[0:2]
    df = df[cols]

    # Display the updated DataFrame
    print("\nUpdated DataFrame with NOMEDISCIPLINA:")
    print(df.head())

    return df


def main():
    # ------------------------------- CE processing ------------------------------- #
    # Specify the folder containing the Excel files
    folder_path = 'data/CE'  # Make sure the folder path is correct

    # Load Excel files and combine them
    ce_combined_data = load_ce_files(folder_path)

    # Display the first few rows of the combined DataFrame
    print("\nCombined Data:")
    print(ce_combined_data.head())

    # Save the combined DataFrame to a new Excel file
    output_file = 'CE_combined.xlsx'
    ce_combined_data.to_excel(output_file, index=False)
    print(f"\nCombined data saved to '{output_file}'")

    # remove duplicates based on the columns "CODDISCIPLINACOD"
    #ce_combined_data_clean = ce_combined_data.drop_duplicates(subset='CODDISCIPLINACOD')

    # Save the combined DataFrame to a new Excel file
    output_file = 'UC_CE.xlsx'
    ce_combined_data.to_excel(output_file, index=False)
    print(f"\nCombined data saved to '{output_file}'")

    # ------------------------------- Msc processing ------------------------------- #
    # Load Master curricular plans and combine them
    msc_combined_master_data = load_master_curricular_plans("data/MSC")

    # save the combined master data to a new Excel file
    output_master_file = 'MSC_combined.xlsx'
    msc_combined_master_data.to_excel(output_master_file, index=False)
    print(f"\nCombined master data saved to '{output_master_file}'")

    # remove duplicates based on the columns "CODDISCIPLINA"
    #msc_combined_master_data_clean = msc_combined_master_data.drop_duplicates(subset='CODDISCIPLINACOD')

    # save the combined master data to a new Excel file
    output_master_file = 'UC_MSC.xlsx'
    msc_combined_master_data.to_excel(output_master_file, index=False)
    print(f"\nCombined master data saved to '{output_master_file}'")

    # ------------------------------- MicroCred processing ------------------------------- #
    # Load the microcredential data
    microcredential_file_path = 'data/Microcredenciais.xlsx'  # Make sure the file path is correct
    microcredential_data = load_microcredentials(microcredential_file_path)

    # Save the microcredential data to a new Excel file
    output_microcredential_file = 'UC_Microcredenciais.xlsx'
    microcredential_data.to_excel(output_microcredential_file, index=False)
    print(f"\nMicrocredential data saved to '{output_microcredential_file}'")

    # ------------------------------- Combined Data processing ------------------------------- #
    # Combine the microcredential data with the master and specialization curricular plans
    uc_data = pd.concat([msc_combined_master_data, ce_combined_data, microcredential_data], ignore_index=True, sort=False)

    # ------------------------------- Add URL column ------------------------------- #
    # Load the link info file
    link_info_file_path = 'DPUCs - contents + objectives.xlsx'
    link_info = pd.read_excel(link_info_file_path)

    # Merge the UC data with the link info on CODDISCIPLINACOD (UC data) and CodigoPACO (link info)
    uc_data = pd.merge(uc_data, link_info[['CodigoPACO', 'Url']], left_on='CODDISCIPLINACOD', right_on='CodigoPACO', how='left')

    # Drop the 'CodigoPACO' column after the merge
    uc_data.drop('CodigoPACO', axis=1, inplace=True)

    # Normalize the 'NOMEDISCIPLINA' column to uppercase
    uc_data['NOMEDISCIPLINA'] = uc_data['NOMEDISCIPLINA'].str.upper()

    # Normalize the 'DEPARTMENT' column to uppercase
    uc_data['DEPARTMENT'] = uc_data['DEPARTMENT'].str.upper()

    # Filter out rows that contain "Opção" in the NOMEDISCIPLINA column
    uc_data = uc_data[~uc_data['NOMEDISCIPLINA'].str.contains("OPÇÃO", na=False)]

    # Keep only the columns you need after the merge
    uc_data = uc_data[['CODDISCIPLINACOD', 'NOMEDISCIPLINA', 'DEPARTMENT', 'MSC', 'RAMO', 'CE', 'Microcredencial', 'Url']]

    # Remove duplicates only if all columns are the same
    uc_data = uc_data.drop_duplicates()

    # Save the uc data to a new Excel file
    output_uc_file = 'UC_all.xlsx'
    uc_data.to_excel(output_uc_file, index=False)
    print(f"\nUC data saved to '{output_uc_file}'")


if __name__ == "__main__":
    main()
