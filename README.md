# Uktob Assignment
This is a Python web app using the Flask and Mysql.
Steps for running the server:
  1. Create a Python virtual environment (https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate that.
  2. Install the project requirements using the command:
     ```pip install -r requirements.txt```
  3. Create an .env file using .env.sample as a guide. Set the values of DATABASE_URL, MODEL_NAME, OPENAI_API_KEY according to your enviornment.
  4. To apply Database migrations use the command ```flask db upgrade```
  5. Run Flask server use the command ```flask run```
  6. The server will be accessable on the URL ``` http://127.0.0.1:5000```

# API Details
1. To add a new Note, following payload will be use:
     ``` {"title":"notes-title", "content": "notes content", "is_active": true}' ```

   example CURL request will be 
      ```
    curl --location 'http://127.0.0.1:5000/notes' \
    --header 'Content-Type: application/json' \
    --data '{"title":"title", "content": "notes content"}'
    ```
3. To get all notes, example CURL request will be:
   ```
   curl --location 'http://127.0.0.1:5000/notes'
   ```
4. To get specific note obj, example CURL request will be:
    ``` curl --location 'http://127.0.0.1:5000/notes/<note_id>' ```
5. To delete any note obj, example CURL request will be:
     ``` curl --location --request DELETE 'http://127.0.0.1:5000/notes/<note_id>' ```
6. To update any note obj, example CURL request will be:
     ```
     curl --location --request PUT 'http://127.0.0.1:5000/notes/<note_id>' \
      --header 'Content-Type: application/json' \
      --data '{"title": "title", "content": "content"}'
    ```
7. To pass the summary to langchain, example CURL request will be
   ```
   curl --location 'http://127.0.0.1:5000/notes/<note_id>/summarize'
   ```

# Langchain Integration Details
Following are the details to integrate langchain into app
1. We will be getting ModelName from .env file.We are using Chatgpt 3.5 as its fast and efficient.
2. We will get the not obj by passing the id from params.
3. LangChain offers a few different strategies to split text into chunks. we will be using ```CharacterTextSplitter``` to split the text and convert the raw text into Document chunks
4. Prompt is a piece of text containing instructions to an LLM. Those instructions are written using natural language and should convey the user’s intent in order to guide the model to produce the output. Typically, robust prompts aligned with the parameters of the model will lead to more precise results.
5. We will create a prompt with PromptTemplate to guide the LLM to summarize the text and how to return the result.
6. LangChain provides a function called ```load_summarize_chain```. This function returns a chain object optimized to perform summarization tasks.
Note the parameter ```chain_type```. It tells how the chain will handle the token limit restrictions and you can use it as ```stuff``` type which send all prompt text to the LLM in a single call.
7. To apply the summarization task just call the method run with the document. The result will be a text summarized according to the prompt text.


