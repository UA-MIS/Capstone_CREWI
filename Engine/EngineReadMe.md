Going to put the Flask API and actual engine logic in here.

SETUP:
Make sure you're in the engine directory
run "python app.py" in zterminal
go to localhost:8000/hello (subject to change based on paths)

Download/install Python 3.10 or later

pip install flask
pip install flask-cors
pip install python-dotenv

Download/install C++
https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170
select X64 version

pip install mysql-python

add .env file


Also, you're going to need the .env file, but we obviously can't put the database credentials in the code. Message me and I'll send you the variables; make sure you name the file ".env" in the engine folder so that the .gitignore won't commit it.