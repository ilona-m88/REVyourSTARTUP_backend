These are the steps to follow to properly initialize this project:
1. Create a virtual enviornment (run this command from the root folder of your workspace)
    a. command: py -m venv .venv

2. Activate the virtual environment (this should always be done whenever working on this project)
    a. command: .venv/scripts/activate

3. Install dependencies
    a. command: py pip install -r requirements.txt
    b. IMPORTANT: If you decide to install any further dependencies for this project, make sure 
            to run the following command: py -m pip freeze > requirements.txt

4. Test that the server runs locally on your machine
    a. cd into the REVyourSTARTUP root directory
    b. Run the following command: py manage.py runserver
    c. By default, and for this project, Django runs on port 8000
    d. press CTRL+c to stop the server once you see the default welcome page

5. To deactivate the virtual environment, simply run the command: deactivate