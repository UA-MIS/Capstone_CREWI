from app.main import app

# WSGI.PY: This is the actual Python file to run for testing (running python wsgi.py in the terminal)

if __name__ == "__main__":
        # change the port if needed, 8000 usually works fine
        app.run(port=8000)