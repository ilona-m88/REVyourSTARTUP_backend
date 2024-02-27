These are the steps to follow to properly initialize this project:
1. Create a virtual enviornment (run this command from the root folder of your workspace)
    - command: `py -m venv .venv`

2. Activate the virtual environment (this should always be done whenever working on this project)
    - command: `.venv/scripts/activate`

3. Install dependencies
    - command: `py pip install -r requirements.txt`
    - IMPORTANT: If you decide to install any further dependencies for this project, make sure 
            to run the following command: `py -m pip freeze > requirements.txt`

4. Test that the server runs locally on your machine
    - Run the following command: `py manage.py runserver`
    - By default, and for this project, Django runs on port 8000
    - press CTRL+c to stop the server once you see the default welcome page

5. To deactivate the virtual environment, simply run the command: `deactivate`