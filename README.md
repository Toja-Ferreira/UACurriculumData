# Program for Processing Curriculum Data

This repository contains a program that processes curriculum data for multiple study programs, including Master Programs (MsC) , Especialization Courses (CE), and Microcredentials (μC). It also provides a web interface to visualize the data.

## Table of Contents

- [Requirements](#requirements)
- [Setup and Running the Program](#setup-and-running-the-program)
  - [Step 1: Set Up Virtual Environment](#step-1-set-up-virtual-environment)
  - [Step 2: Run the Branch Processing Script](#step-2-run-the-branch-processing-script)
  - [Step 3: Run the Main Processing Script](#step-3-run-the-main-processing-script)
  - [Step 4: Start the Streamlit App](#step-4-start-the-streamlit-app)
- [Accessing the Website](#accessing-the-website)

## Requirements

Ensure you have the following installed on your system:

- Python 3.8+
- Virtualenv (optional but recommended)

## Setup and Running the Program

### Step 1: Set Up Virtual Environment

1. Clone the repository to your local machine:

   ```
   bash
   git clone git@github.com:Toja-Ferreira/UACurriculumData.git
   cd UACurriculumData
   ```

2. Create a virtual environment:

   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```
     .\venv\Scripts\activate
     ```

   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies from `requirements.txt`:

   ```
   pip install -r requirements.txt
   ```

### Step 2: Run the Branch Processing Script

The first step in processing is dealing with Master Programs with multiple branches. Run the `msc_branch_processing.py` script as follows:

   ```
   python3 msc_branch_processing.py
   ```

### Step 3: Run the Main Processing Script

Once the branch processing is complete, execute `main.py` to process all study programs (Master, Continuing Education, Microcredentials):

   ```
   python3 main.py
   ```

### Step 4: Start the Streamlit App

Finally, launch the Streamlit application to visualize the processed data on a local server:

   ```
   streamlit run showdata.py
   ```
## Accessing the Website

After running the above command, the web application should open in your browser at:
`http://localhost:8501`

If you prefer not to run the program locally, you can access the same Streamlit application online:

[https://uacurriculumdata.streamlit.app/](https://uacurriculumdata.streamlit.app/)
