### CREWI Engine ReadMe

This folder contains engine for the CREWI project.

Make sure to refer to the setup video to get everything up and running for local testing.


### Environment Variables

There are three ways to get the environment variables that are referenced in the set-up video:
1. Go to this UA Box link (which will require a UA log-in) and download the file (be sure to name it `.env`): https://alabama.box.com/s/ppldcpifoo139sje8l4y91qwch3afdv6
2. Log into the engine Heroku server and copy the configuration variables from there
3. Log into Google Drive with the Capstone Crewi gmail account and download the file from there (you may have to enable third-party cookies, and make sure to name it `.env`)


### Running the Engine Locally

Once you've followed the setup instructions, running the engine locally should be fairly straightforward:
1. `python wsgi.py` will run the engine locally
2. Send requests to the localhost URL plus /recommendation to test
3. The localhost URL itself (the base path, with no routing, basically) will reveal request format requirements if needed


### Updating Requirements

If you need new Python packages, make sure to add them as dependencies in requirements.txt and the Pipfile. There are commands for this, but there's a bug with pipreqs (which is a package that does this automatically), so our current recommendation would be to do this manually.


### `python FILENAME`

Runs whatever python file is given; for this engine, `python wsgi.py` is the only one necessary.


### `pip install PACKAGENAME`

Installs whatever package is given; the setup should cover the initially required packages. Make sure to add new requirements to requirements.txt and Pipfile (either manually or using commands).


### `pipenv install PACKAGENAME`

Installs the package in a virtual pip environment. This shouldn't be necessary for the most part because the virtual environment is mostly for deployment. With that said, you can try installing things this way if requirements aren't being found.


### `pip install -r requirements.txt`

Installs all the packages in requirements.txt. This shouldn't need to be run often, but occasionally doing it might solve bugs across different machines. It functions like `npm install`, but for the back-end.


### `pipenv install -r requirements.txt`

Installs all the packages in requirements.txt in the virtual environment. This shouldn't need to be run often, but occasionally doing it might solve bugs across different machines. It functions like `npm install`, but for the back-end.
