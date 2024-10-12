import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import plotly.graph_objects as go

plt.rcParams['font.family'] = 'serif'

# Set the theme to light mode in the app
st.set_page_config(page_title="University Curriculum Data", layout="wide", page_icon="📊", initial_sidebar_state="expanded")

# Define a color palette for consistency
color_palette = {
    'MsC': '#FF4B4B',
    'CE': '#4BFF6B',
    'μC': '#4BB0FF'
}

# Load your data
uc_data = pd.read_excel('UC_all.xlsx')

original_data = uc_data.copy()

# Initialize uc_data in session state if it doesn't exist
if 'uc_data' not in st.session_state:
    st.session_state.uc_data = uc_data

# Ensure CODDISCIPLINACOD is treated as a string to avoid commas in the display
st.session_state.uc_data['CODDISCIPLINACOD'] = uc_data['CODDISCIPLINACOD'].astype(str)

# Convert CODIGOMICROCREDENCIAL to string and format it
st.session_state.uc_data['CODIGOMICROCREDENCIAL'] = uc_data['CODIGOMICROCREDENCIAL'].apply(lambda x: f"{int(x)}" if pd.notnull(x) else "")

# Streamlit app layout
st.title("University Curriculum Data Dashboard")

# Create tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs(["General Overview", "Department Overview", "Discipline Overview", "Upload Data"])

# General Overview Tab
with tab1:
    st.header("General Overview of University Curriculum")

    # Total statistics for MsC, CE, and Microcredentials
    unique_msc_count = st.session_state.uc_data['MSC'].nunique()
    unique_msc_disciplines = st.session_state.uc_data[st.session_state.uc_data['MSC'].notna()]['CODDISCIPLINACOD'].nunique()

    unique_ce_count = st.session_state.uc_data['CE'].nunique()
    unique_ce_disciplines = st.session_state.uc_data[st.session_state.uc_data['CE'].notna()]['CODDISCIPLINACOD'].nunique()

    unique_micro_count = st.session_state.uc_data['Microcredencial'].nunique()  # This is always 1:1, so no need for discipline count

    # Display program counts and disciplines
    st.write(f"### Total Programs and Disciplines Across University")
    st.write(f"- **{unique_msc_count}** Master programs (MsC) with **{unique_msc_disciplines}** disciplines.")
    st.write(f"- **{unique_ce_count}** Especialization programs (CE) with **{unique_ce_disciplines}** disciplines.")
    st.write(f"- **{unique_micro_count}** Microcredentials (μC).")

    # Overlapping disciplines between MsC, CE, and Microcredentials
    msc_disciplines = set(st.session_state.uc_data[st.session_state.uc_data['MSC'].notna()]['CODDISCIPLINACOD'].unique())
    ce_disciplines = set(st.session_state.uc_data[st.session_state.uc_data['CE'].notna()]['CODDISCIPLINACOD'].unique())
    micro_disciplines = set(st.session_state.uc_data[st.session_state.uc_data['Microcredencial'].notna()]['CODDISCIPLINACOD'].unique())

    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        fig, ax = plt.subplots(figsize=(6, 6))  # Keep a reasonable size for Venn diagram
        # Add title to the Venn diagram
        ax.set_title('Disciplines of UA', fontsize=16)
        venn = venn3([msc_disciplines, ce_disciplines, micro_disciplines], ('MsC', 'CE', 'μC'))

        # Update labels as needed
        if venn.get_label_by_id('100'):
            venn.get_label_by_id('100').set_text(f'{len(msc_disciplines - ce_disciplines - micro_disciplines)}')
        if venn.get_label_by_id('010'):
            venn.get_label_by_id('010').set_text(f'{len(ce_disciplines - msc_disciplines - micro_disciplines)}')
        if venn.get_label_by_id('001'):
            venn.get_label_by_id('001').set_text(f'{len(micro_disciplines - msc_disciplines - ce_disciplines)}')
        if venn.get_label_by_id('110'):
            venn.get_label_by_id('110').set_text(f'{len(msc_disciplines & ce_disciplines - micro_disciplines)}')
        if venn.get_label_by_id('011'):
            venn.get_label_by_id('011').set_text(f'{len(ce_disciplines & micro_disciplines - msc_disciplines)}')
        if venn.get_label_by_id('101'):
            venn.get_label_by_id('101').set_text(f'{len(msc_disciplines & micro_disciplines - ce_disciplines)}')
        if venn.get_label_by_id('111'):
            venn.get_label_by_id('111').set_text(f'{len(msc_disciplines & ce_disciplines & micro_disciplines)}')

        # Set colors for the circles in the Venn diagram based on region IDs
        venn_colors = {
            '100': color_palette['MsC'],                # MSC only
            '010': color_palette['CE'],                 # CE only
            '001': color_palette['μC'],                 # μC only
        }

        # Apply colors to patches, but only if the patch (region) exists
        region_labels = ['100', '010', '001']  # Corresponding region IDs

        for region_id in region_labels:
            patch = venn.get_patch_by_id(region_id)
            if patch is not None:  # Only apply color if the region exists
                patch.set_facecolor(venn_colors[region_id])
                patch.set_alpha(1)  # Adjust transparency
                patch.set_antialiased(True)
                
        st.pyplot(fig)

    # Interpret the Venn diagram and explain the overlaps
    st.subheader("Interpretation of Discipline Overlaps")
    
    overlapping_msc_ce = len(msc_disciplines & ce_disciplines - micro_disciplines)
    overlapping_ce_micro = len(ce_disciplines & micro_disciplines - msc_disciplines)
    overlapping_msc_micro = len(msc_disciplines & micro_disciplines - ce_disciplines)
    overlapping_all_three = len(msc_disciplines & ce_disciplines & micro_disciplines)

    # Generate the explanation text dynamically
    explanation_text = f"""
    - **{len(msc_disciplines - ce_disciplines - micro_disciplines)}** disciplines are exclusive to **Master programs (MsC)**.
    - **{len(ce_disciplines - msc_disciplines - micro_disciplines)}** disciplines are exclusive to **Especialization programs (CE)**.
    - **{len(micro_disciplines - msc_disciplines - ce_disciplines)}** disciplines are exclusive to **Microcredentials (μC)**.
    - **{overlapping_msc_ce}** disciplines overlap between **MsC and CE** but **NOT** with **μC**.
    - **{overlapping_ce_micro}** disciplines overlap between **CE and μC** but **NOT** with **MsC**.
    - **{overlapping_msc_micro}** disciplines overlap between **MsC and μC** but **NOT** with **CE**.
    - **{overlapping_all_three}** disciplines are common across **MsC, CE, and μC**.
    """
    st.write(explanation_text)

# Department Overview Tab
with tab2:
    st.header("Department Overview")

    # Interactivity: Filter by department
    department_filter = st.selectbox("Select a Department:", st.session_state.uc_data['DEPARTMENT'].unique())

    filtered_data = st.session_state.uc_data[st.session_state.uc_data['DEPARTMENT'] == department_filter].drop_duplicates()

    if len(filtered_data) > 0:
        # Display the data
        st.write(f"### UC's for Department: {department_filter}")

        # Drop the DEPARTMENT column from the filtered data
        filtered_display_data = filtered_data.drop(columns=['DEPARTMENT'])

        # Drop the Url column from the filtered data
        #filtered_display_data = filtered_data.drop(columns=['Url'])

        # Sort the DataFrame by the CODDISCIPLINA column
        filtered_display_data = filtered_display_data.sort_values(by='CODDISCIPLINACOD')

        st.dataframe(filtered_display_data, use_container_width=True, hide_index=True)

        # Count unique courses for each category
        msc_courses = set(filtered_data['MSC'].dropna().unique())  # Unique MsC courses
        ce_courses = set(filtered_data['CE'].dropna().unique())  # Unique CE courses
        micro_courses = set(filtered_data['Microcredencial'].dropna().unique())  # Unique Microcredentials
        
        msc_courses_count = len(msc_courses)  # Count unique MsC courses
        ce_courses_count = len(ce_courses)  # Count unique CE courses
        micro_courses_count = len(micro_courses)  # Count unique Microcredentials
        
        # Count unique disciplines for each category
        msc_disciplines = set(filtered_data[filtered_data['MSC'].notna()]['CODDISCIPLINACOD'].unique())
        ce_disciplines = set(filtered_data[filtered_data['CE'].notna()]['CODDISCIPLINACOD'].unique())
        micro_disciplines = set(filtered_data[filtered_data['Microcredencial'].notna()]['CODDISCIPLINACOD'].unique())

        msc_disciplines_count = len(msc_disciplines)
        ce_disciplines_count = len(ce_disciplines)
        micro_disciplines_count = len(micro_disciplines)

        # Display department-specific counts with formatted text
        st.write(f"### Summary of Programs in {department_filter}:")
        st.write(f"- **{msc_courses_count}** Master programs (MsC) with **{msc_disciplines_count}** disciplines.")
        
        # List all Master Programs in an expander
        if msc_courses_count > 0:
            with st.expander("List of MsC Programs"):
                for program in msc_courses:
                    parts = program.split('_')
                    program_code = parts[0].strip()  # Remove any extra spaces
                    program_name = parts[1].strip().upper()  # Uppercase for uniformity
                    
                    # Check if the program has any branches and gather them
                    program_branches = filtered_data[filtered_data['MSC'] == program]['RAMO'].dropna().unique()
                    
                    # If branches exist, format them with enumeration
                    if program_branches.size > 0:
                        branches_str = ', '.join([branch.replace('_', ' ').strip().upper() for branch in program_branches])
                        st.write(f"**{program_code}** {program_name} (**Branches**: {branches_str})")  # Display program code and name with branches
                    else:
                        st.write(f"**{program_code}** {program_name}")  # No branches

        st.write(f"- **{ce_courses_count}** Especialization programs (CE) with **{ce_disciplines_count}** disciplines.")
        
        # List all CE programs in an expander
        if ce_courses_count > 0:
            with st.expander("List of CE Programs"):
                for program in ce_courses:
                    parts = program.split('_')
                    program_code = parts[0]
                    program_name = parts[1].upper()
                    st.write(f"**{program_code}** {program_name}")

        st.write(f"- **{micro_courses_count}** Microcredentials (μC).")

        # List all Microcredential programs in an expander
        if micro_courses_count > 0:
            with st.expander("List of μC Programs"):
                for program in micro_courses:
                    # Get the corresponding microcredential code from the DataFrame
                    code = int(filtered_data[filtered_data['Microcredencial'] == program]['CODIGOMICROCREDENCIAL'].values[0])
                    # Get the corresponding name from the DataFrame (assuming it's in the same row)
                    name = filtered_data[filtered_data['Microcredencial']  == program]['NOMEDISCIPLINA'].values[0].upper()  # Adjust if necessary
                    st.write(f"**{code}** {name}")

        # Create a bar chart for unique disciplines
        chart_data = pd.DataFrame({
            "Category": ["MsC", "CE", "μC"],
            "Discipline Count": [msc_disciplines_count, ce_disciplines_count, micro_disciplines_count]
        })

        # Create a 2-column layout for the bar chart and pie chart
        col1, col2 = st.columns([1, 0.6])

        # Bar chart for unique disciplines (on the left)
        with col1:
            fig = px.bar(
                chart_data,
                x="Category",
                y="Discipline Count",
                color="Category",  # Map the category to color
                text="Discipline Count",
                title=f"Disciplines by Category in {department_filter}",
                color_discrete_map=color_palette  # Apply color palette here
            )
            fig.update_traces(textposition='outside')  # No need to set marker color here
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

        # Pie chart for discipline distribution (on the right)
        with col2:
            pie_chart_data = {
                'MsC': msc_disciplines_count,
                'CE': ce_disciplines_count,
                'μC': micro_disciplines_count
            }
            # Define the color palette explicitly for each category
            color_discrete_map = {
                'MsC': color_palette['MsC'],
                'CE': color_palette['CE'],
                'μC': color_palette['μC']
            }

            # Use a pie chart but include all categories, even with zero values
            pie_fig = px.pie(
                names=list(pie_chart_data.keys()),
                values=list(pie_chart_data.values()),
                title=f"Discipline Distribution in {department_filter}",
                hole=0.6,
                color=list(pie_chart_data.keys()),  # Use the category names for coloring
                color_discrete_map=color_discrete_map  # Explicit color mapping
            )
            pie_fig.update_traces(textinfo='percent+label')

            st.plotly_chart(pie_fig)

        # Prepare data for Venn diagram
        sets = [msc_disciplines, ce_disciplines, micro_disciplines]
        labels = ['MsC' if len(msc_disciplines) > 0 else '',
                  'CE' if len(ce_disciplines) > 0 else '',
                  'μC' if len(micro_disciplines) > 0 else '']

        # Initialize overlapping variables
        overlapping_msc_only = set()
        overlapping_ce_only = set()
        overlapping_micro_only = set()
        overlapping_msc_ce = set()
        overlapping_ce_micro = set()
        overlapping_msc_micro = set()
        overlapping_all = set()

        # Create a Venn diagram only if there is at least one non-empty set
        if any(len(discipline) > 0 for discipline in sets):
            fig, ax = plt.subplots(figsize=(6, 6))
            # Add title to the Venn diagram
            ax.set_title(f'Overlap of Disciplines in {department_filter}', fontsize=16)
            venn = venn3(subsets=sets, set_labels=labels)

            # Calculate overlapping disciplines
            overlapping_msc_only = msc_disciplines - ce_disciplines - micro_disciplines
            overlapping_ce_only = ce_disciplines - msc_disciplines - micro_disciplines
            overlapping_micro_only = micro_disciplines - msc_disciplines - ce_disciplines
            overlapping_msc_ce = msc_disciplines & ce_disciplines - micro_disciplines
            overlapping_ce_micro = ce_disciplines & micro_disciplines - msc_disciplines
            overlapping_msc_micro = msc_disciplines & micro_disciplines - ce_disciplines
            overlapping_all = msc_disciplines & ce_disciplines & micro_disciplines

            # Limit the width of the container to reduce the visual size of the Venn diagram
            col1, col2, col3 = st.columns([1, 2, 1])  # Create columns with different width ratios

            with col2:
                # Safely set labels by checking if they exist first
                if venn.get_label_by_id('100'):
                    venn.get_label_by_id('100').set_text(f'{len(overlapping_msc_only)}')
                if venn.get_label_by_id('010'):
                    venn.get_label_by_id('010').set_text(f'{len(overlapping_ce_only)}')
                if venn.get_label_by_id('001'):
                    venn.get_label_by_id('001').set_text(f'{len(overlapping_micro_only)}')
                if venn.get_label_by_id('110'):
                    venn.get_label_by_id('110').set_text(f'{len(overlapping_msc_ce)}')
                if venn.get_label_by_id('011'):
                    venn.get_label_by_id('011').set_text(f'{len(overlapping_ce_micro)}')
                if venn.get_label_by_id('101'):
                    venn.get_label_by_id('101').set_text(f'{len(overlapping_msc_micro)}')
                if venn.get_label_by_id('111'):
                    venn.get_label_by_id('111').set_text(f'{len(overlapping_all)}')

                # Set colors for the circles in the Venn diagram based on region IDs
                venn_colors = {
                    '100': color_palette['MsC'],                # MSC only
                    '010': color_palette['CE'],                 # CE only
                    '001': color_palette['μC'],                 # μC only
                }

                # Apply colors to patches, but only if the patch (region) exists
                region_labels = ['100', '010', '001']  # Corresponding region IDs

                for region_id in region_labels:
                    patch = venn.get_patch_by_id(region_id)
                    if patch is not None:  # Only apply color if the region exists
                        patch.set_facecolor(venn_colors[region_id])
                        patch.set_alpha(1)  # Adjust transparency
                        patch.set_antialiased(True)

                st.pyplot(fig)

            # Create a mapping of disciplines to their respective programs (MsC, CE, Microcredentials)
            discipline_to_program = {
                discipline: {
                    'MsC': filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline]['MSC'].dropna().unique().tolist(),
                    'CE': filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline]['CE'].dropna().unique().tolist(),
                    'μC': filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline]['Microcredencial'].dropna().unique().tolist(),
                }
                for discipline in set(filtered_data['CODDISCIPLINACOD'])
            }

            # Initialize a list to hold explanations and their corresponding disciplines
            explanations_with_disciplines = []

            # Prepare explanations with counts and empty lists for disciplines
            if len(overlapping_msc_only) > 0:
                explanations_with_disciplines.append(
                    (f"- **MsC Only**: **{len(overlapping_msc_only)}** disciplines exclusive to **Master programs (MsC)**.", overlapping_msc_only)
                )
            if len(overlapping_ce_only) > 0:
                explanations_with_disciplines.append(
                    (f"- **CE Only**: **{len(overlapping_ce_only)}** disciplines exclusive to **Especialization programs (CE)**.", overlapping_ce_only)
                )
            if len(overlapping_micro_only) > 0:
                explanations_with_disciplines.append(
                    (f"- **μC Only**: **{len(overlapping_micro_only)}** disciplines exclusive to **Microcredentials (μC)**.", overlapping_micro_only)
                )
            if len(overlapping_msc_ce) > 0:
                explanations_with_disciplines.append(
                    (f"- **MsC and CE Only**: **{len(overlapping_msc_ce)}** disciplines shared between **MsC** and **CE** programs, but **NOT** with **μC**.", overlapping_msc_ce)
                )
            if len(overlapping_ce_micro) > 0:
                explanations_with_disciplines.append(
                    (f"- **CE and μC Only**: **{len(overlapping_ce_micro)}** disciplines shared between **CE** programs and **μC**, but **NOT** with **MsC** programs.", overlapping_ce_micro)
                )
            if len(overlapping_msc_micro) > 0:
                explanations_with_disciplines.append(
                    (f"- **MsC and μC Only**: **{len(overlapping_msc_micro)}** disciplines shared between **MsC** and **μC**, but **NOT** with **CE** programs.", overlapping_msc_micro)
                )
            if len(overlapping_all) > 0:
                explanations_with_disciplines.append(
                    (f"- **MsC, CE and μC**: **{len(overlapping_all)}** disciplines common across **MsC, CE and μC**.", overlapping_all)
                )

            # Display the explanation and lists directly after each count
            for explanation, disciplines in explanations_with_disciplines:
                st.markdown(explanation)  # Display the explanation
                
                # Create an expander for the overlapping disciplines
                with st.expander("Discipline List"):
                    # List the overlapping disciplines
                    for discipline in disciplines:
                        # Get the discipline name and URL from the DataFrame
                        discipline_row = filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline].iloc[0]
                        discipline_name = discipline_row['NOMEDISCIPLINA']
                        url = discipline_row['Url']

                        # Display discipline code and name as a clickable link that opens in a new tab
                        st.markdown(f"**{discipline}**: <a href='{url}' target='_blank'>**{discipline_name}**</a>", unsafe_allow_html=True)


            # Create a mapping of disciplines to their respective programs (MsC, CE, Microcredentials)
            discipline_to_program = {
                discipline: {
                    'MsC': filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline]['MSC'].dropna().unique().tolist(),
                    'CE': filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline]['CE'].dropna().unique().tolist(),
                    'μC': filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline]['Microcredencial'].dropna().unique().tolist(),
                }
                for discipline in set(filtered_data['CODDISCIPLINACOD'])
            }

            # Helper function to add each overlapping discipline along with expanders for the programs
            def add_overlap(discipline):
                # Get the discipline name and URL
                discipline_data = filtered_data[filtered_data['CODDISCIPLINACOD'] == discipline]
                discipline_name = discipline_data['NOMEDISCIPLINA'].values[0]
                discipline_url = discipline_data['Url'].values[0]  # Assume there's a URL column in your filtered_data

                # Display the discipline code and name as a hyperlink
                st.markdown(f"**{discipline}: <a href='{discipline_url}' target='_blank'>{discipline_name}</a>**", unsafe_allow_html=True)
                
                # Get the programs related to the discipline
                programs = discipline_to_program.get(discipline, {})
                
                # Expander for MsC Programs
                if programs['MsC']:
                    with st.expander(f"MsC Programs:"):
                        for program in programs['MsC']:
                            # Extract the master program name from the MSC column
                            master_program = filtered_data[filtered_data['MSC'] == program]['MSC'].values[0]
                            parts = master_program.split('_')
                            program_code = parts[0]
                            program_name = parts[1].upper()
                            st.write(f"- **{program_code} -** {program_name}")
                
                # Expander for Microcredentials
                if programs['μC']:
                    with st.expander(f"μC Programs:"):
                        for microcred in programs['μC']:
                            # Extract the microcredential name from the column
                            microcred_code = int(filtered_data[filtered_data['Microcredencial'] == microcred]['CODIGOMICROCREDENCIAL'].values[0])
                            microcred_name = filtered_data[filtered_data['Microcredencial'] == microcred]['NOMEDISCIPLINA'].values[0]
                            st.write(f"- **{microcred_code} -** {microcred_name}")

                # Expander for CE Programs
                if programs['CE']:
                    with st.expander(f"CE Programs:"):
                        for program in programs['CE']:
                            ce_program = filtered_data[filtered_data['CE'] == program]['CE'].values[0]
                            parts = ce_program.split('_')
                            program_code = parts[0]
                            program_name = parts[1].upper()
                            st.write(f"- **{program_code} -** {program_name}")

            # Add overlapping disciplines and their corresponding programs
            if overlapping_msc_ce:
                st.write("#### Overlapping Disciplines between MsC and CE:")
                for discipline in overlapping_msc_ce:
                    add_overlap(discipline)

            if overlapping_ce_micro:
                st.write("#### Overlapping Disciplines between CE and μC:")
                for discipline in overlapping_ce_micro:
                    add_overlap(discipline)

            if overlapping_msc_micro:
                st.write("#### Overlapping Disciplines between MsC and μC:")
                for discipline in overlapping_msc_micro:
                    add_overlap(discipline)

            if overlapping_all:
                st.write("#### Overlapping Disciplines between MsC, CE, and μC:")
                for discipline in overlapping_all:
                    add_overlap(discipline)

    else:
        st.write("No data available for the selected department.")

# Discipline Overview Tab
with tab3:
    st.header("Discipline Overview")

    # Remove duplicates based on 'NOMEDISCIPLINA' and 'CODDISCIPLINACOD' columns to populate the selectbox
    unique_disciplines = st.session_state.uc_data[['NOMEDISCIPLINA', 'CODDISCIPLINACOD']].drop_duplicates()

    # Combine search and dropdown into one selectbox for unique disciplines
    discipline_selection = st.selectbox(
        "Search or Select a Discipline by its code (CODDISCIPLINACOD) or name (NOMEDISCIPLINA):",
        unique_disciplines['NOMEDISCIPLINA'] + " (" + unique_disciplines['CODDISCIPLINACOD'] + ")"
    )

    if discipline_selection:
        # Extract the selected discipline information
        discipline_code = discipline_selection.split(" (")[1][:-1]  # Extract the discipline code from the selection
        selected_discipline_data = st.session_state.uc_data[st.session_state.uc_data['CODDISCIPLINACOD'] == discipline_code]

        # Display discipline details (name and code)
        discipline_name = selected_discipline_data['NOMEDISCIPLINA'].iloc[0]
        url = selected_discipline_data['Url'].iloc[0]  # Get the URL for the selected discipline
            
        # Display discipline details (name and code) with a hyperlink
        st.markdown(f"### Discipline: <a href='{url}' target='_blank'>**{discipline_name}**</a> ({discipline_code})", unsafe_allow_html=True)

        ### Handling the MSC, CE, and Microcredentials Program Display ###

        # 1. Master's (MsC) programs
        if selected_discipline_data['MSC'].notna().any():
            msc_courses = selected_discipline_data[selected_discipline_data['MSC'].notna()]
            # Group by the MsC code (program) and aggregate branches
            msc_grouped = msc_courses.groupby('MSC')['RAMO'].apply(
                lambda x: ' - '.join(f"[{str(i).replace('_', ' ').upper()}]" for i in sorted(set(x)) if pd.notna(i))
            ).reset_index()

            st.markdown(f"### {len(msc_grouped)} Master Programs (MsC)")
            with st.expander("MsC List"):
                for index, row in msc_grouped.iterrows():
                    parts = row['MSC'].split('_')
                    program_code = parts[0]
                    program_name = parts[1].upper()
                    branches = row['RAMO']  # Concatenated branches for this program
                    
                    # Only show branches if they exist
                    if branches:  # If branches are not empty
                        branch_list = [branch.strip() for branch in branches.split('-')]
                        branch_count = len(branch_list)  # Count the number of branches
                        
                        st.write(f"- **{program_code} -** {program_name}")
                        st.write(f"**{branch_count} Ramos:** {branches}")
                    else:
                        st.write(f"- **{program_code} -** {program_name}")  # No branches

        # 2. Continuing Education (CE) programs
        if selected_discipline_data['CE'].notna().any():
            ce_courses = selected_discipline_data[selected_discipline_data['CE'].notna()]
            # Group by the CE code (program) and aggregate branches
            ce_grouped = ce_courses.groupby('CE').apply(
                lambda x: ', '.join(sorted(set(str(i).replace('_', ' ').upper() for i in x if pd.notna(i))))  # Uppercase and remove underscores
            ).reset_index()

            st.markdown(f"### {len(ce_grouped)} Especialization Programs (CE)")
            with st.expander("CE List"):
                for index, row in ce_grouped.iterrows():
                    parts = row['CE'].split('_')
                    ce_code = parts[0]
                    ce_name = parts[1].upper()

                    st.write(f"- **{ce_code} -** {ce_name}")

        # 3. Microcredentials
        if selected_discipline_data['Microcredencial'].notna().any():
            micro_courses = selected_discipline_data[selected_discipline_data['Microcredencial'].notna()]
            # Group by the CE code (program) and aggregate branches
            micro_grouped = ce_courses.groupby('CODIGOMICROCREDENCIAL').apply(
                lambda x: ', '.join(sorted(set(str(i).replace('_', ' ').upper() for i in x if pd.notna(i))))  # Uppercase and remove underscores
            ).reset_index()

            st.markdown(f"### {len(micro_grouped)} Microcredential Programs (μC)")
            with st.expander("μC List"):
                for index, course in micro_courses.iterrows():
                    microcred_code = int(course['CODIGOMICROCREDENCIAL'])
                    microcred_name = course['NOMEDISCIPLINA']
                    st.write(f"- **{microcred_code} -** {microcred_name}")

# Upload Data Tab
with tab4:
    st.header("Upload Excel Files to Update Data")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'], accept_multiple_files=False)

    if st.button("Update Data"):
        if uploaded_file:
            # Read the uploaded Excel file into uc_data
            uc_data = pd.read_excel(uploaded_file)

            # Check if uc_data has the same columns as original data
            if set(uc_data.columns) == set(original_data.columns):
                # Save the new uc_data to session state
                st.session_state.uc_data = uc_data
                st.success(f"Data from {uploaded_file.name} has been loaded successfully.")
            else:
                st.error(f"The uploaded file {uploaded_file.name} does not have the correct columns.")
        else:
            st.warning("Please upload a file.")

    # Display the current uc_data if it exists
    if st.session_state.uc_data is not None:
        st.dataframe(st.session_state.uc_data, use_container_width=True, hide_index=True)