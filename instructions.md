How to Run the Setup Script

**1-)** Open your terminal and navigate to the project folder:

`cd /path/to/project`

## For _Linux/Mac_

**2-)** Make the script executable (only once, if needed):

`chmod +x init.sh`

Run the script using source to ensure the install requirements and virtual environment activates in your current shell:

`source init.sh`

## For _Windows Powershell_

**2-)** If you haven’t allowed running scripts yet, run this once to enable script execution (you might need to run PowerShell as Administrator):

`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

Run the setup script to create virtual environment and install requirements:

`.\init.ps1`

To activate the virtual environment later manually, run:

`.\venv\Scripts\Activate.ps1`


**3-)** After finishing the setup, you can start the project with:

`uvicorn main:app --reload`
