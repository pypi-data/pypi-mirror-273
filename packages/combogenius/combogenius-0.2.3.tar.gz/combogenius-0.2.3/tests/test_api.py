from combogenius.api.api import run_api
import sys
import io

# Redirect stdout to capture uvicorn output
sys.stdout = io.StringIO()

def test_api():
    try:
        run_api()
        # If run_api runs without raising exceptions, assert True
        assert True
    except Exception as e:
        # If an exception is raised, assert False and print the error
        assert False, f"An exception occurred: {e}"

# Reset stdout
sys.stdout = sys.__stdout__