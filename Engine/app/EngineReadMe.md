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