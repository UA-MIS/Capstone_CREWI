## Update: run python wsgi.py (in Engine folder); everything else should be fine

# To update requirements file: run pipreqs (in Engine folder); if pipreqs isn't installed run pip install pipreqs (in Engine folder)
# If you update the requirements file, you must update the Pipfile: run pipenv install -r requirements.txt (in Engine folder), then pipenv shell (also in Engine folder) to update the virtual environment

# To install requirements: run pip install -r requirements.txt (in Engine folder)

Going to put the Flask API and actual engine logic in here.

SETUP:
download Python 3.10 from MS Store
enter command "pip install flask-cors" in terminal
enter command "pip install dotenv" in VS terminal

Make sure you're in the engine directory
run "python app.py" in zterminal
go to localhost:8000/hello (subject to change based on paths)

Download/install Python 3.10 or later

To install all the requirements, run ```pip install -r requirements.txt```

pip install flask
pip install flask-cors
pip install python-dotenv

Download/install C++
https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170
select X64 version

pip install mysql-connector-python


add .env file

Here's a link to a UA box folder for the project (requires a UA sign-in):
https://alabama.box.com/s/y78iqm7o7lw3c6f8b9s9uoflzwa2diu8

Here's a link directly to the .env file (also requires a UA sign-in):
https://alabama.box.com/s/ppldcpifoo139sje8l4y91qwch3afdv6




Also, you're going to need the .env file, but we obviously can't put the database credentials in the code. Message me and I'll send you the variables; make sure you name the file ".env" in the engine folder so that the .gitignore won't commit it.

# Definitive Setup Guide (3/24/22):

Step 1: Go to https://www.python.org/downloads/ and download/install the latest version

Step 2: Clone the code from https://github.com/UA-MIS/Capstone_CREWI onto your machine

Step 3: Open a terminal and navigate to the Capstone_CREWI directory

Step 4: Navigate to /Capstone_CREWI/Engine

Step 5: Run ```pip install -r requirements.txt``` (this installs all the requirements in the requirements.txt file)

Step 6: Go to https://alabama.box.com/s/ppldcpifoo139sje8l4y91qwch3afdv6 and download the .env file

Step 7: Copy the .env file into the /Capstone_CREWI/Engine/app folder (this is just a text file, so you can just make a file called .env and paste in the text if needed)

Step 6: Run ```python wsgi.py``` to run the engine locally (it runs on port 8000; this can be changed in the file, but the default port is busy on the AIME computers)

Step 7: Open http://localhost:8000/ (swap port number if needed) to view the home page of the engine, which has documentation on formatting a request

Notes:
    > We recommend using Postman for 