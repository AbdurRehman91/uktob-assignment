# uktob-assignment
Steps for running the server:
  1. Create a Python virtual environment (https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate that.
  2. Install the project requirements using the command:
     ```pip install -r requirements.txt```
  3. Create an .env file using .env.sample as a guide. Set the values of DATABASE_URL, MODEL_NAME, OPENAI_API_KEY according to your enviornment.
  4. To apply Database migrations use the command ```flask db upgrade```
  5. Run Flask server use the command ```flask run```




