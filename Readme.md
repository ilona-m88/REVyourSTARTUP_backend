These are the steps to follow to properly initialize this project:

1. Create a virtual environment (run this command from the root folder of your workspace)

   - command: `py -m venv .venv`

2. Activate the virtual environment (this should always be done whenever working on this project)

   - command: `.venv/scripts/activate`

3. Install dependencies

   - command: `pip install -r requirements.txt`
   - IMPORTANT: If you decide to install any further dependencies for this project, make sure
     to run the following command: `py -m pip freeze > requirements.txt`

4. Test that the server runs locally on your machine

   - Run the following command: `py manage.py runserver`
   - By default, and for this project, Django runs on port 8000
   - press CTRL+c to stop the server once you see the default welcome page

5. To deactivate the virtual environment, simply run the command: `deactivate`

6. IMPORTANT ADDITION: You must create and initialize the MySQL database
   - First, run the file dbSchema.sql
   - Second, create a file named `.env` within the `REVyourSTARTUP` directory. This file will contain the appropriate environment variables required for Django to connect to the database. THIS FILE IS PART OF `.gitignore`, and as such it is important that you set it up correctly.
   - Here are the contents of the file:
     ```
     SECRET_KEY=django-insecure-)qg200wnf_rtwaw#7lkh9eg6j4j--_gj1rbsin*$^%o6356h#*
     DATABASE_NAME=revstartup
     DATABASE_USER=root
     DATABASE_PASS=YOUR PASSWORD GOES HERE!!!!
     ```
   - Replace DATABASE_PASS with the one you have created on your system for your local MySQL server
