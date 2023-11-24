import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
#from langchain.chain.summerize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from .settings.config import DevelopmentConfig, ProductionConfig
from .models.notes import db, Notes
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db.init_app(app) #Add this line Before migrate line
migrate = Migrate(app, db)

# API Endpoint for creating a new note
@app.route('/notes', methods=['POST'])
def create_note():
    try:
        data = request.get_json()
        new_note = Notes(title=data['title'], content=data['content'])
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'message': 'Note created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API Endpoint for getting all notes
@app.route('/notes', methods=['GET'])
def get_all_notes():
    notes = Notes.query.filter_by(is_active=True).all()
    notes_list = [{'id': note.id, 'title': note.title, 
                   'content': note.content,
                    'is_active': note.is_active, 'created': note.created_at, 
                    'updated':note.updated_at} for note in notes]
    return jsonify({'notes': notes_list})

# API Endpoint for getting a specific note by ID
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    try:
        note = Notes.query.get(note_id)
        if note:
            return jsonify({'id': note.id, 'title': note.title, 
                            'content': note.content, 'is_active': note.is_active, 
                            'created': note.created_at, 'updated':note.updated_at})
        return jsonify({'error': 'Note not found'}), 404
    except Exception as e:

        return jsonify({'error': str(e)}), 500

# API Endpoint for deleting a note by ID
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        note = Notes.query.get(note_id)
        if note:
            note.is_active = False
            db.session.commit()
            return jsonify({'message': 'Note deleted successfully'})
        else:
            return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Endpoint for updating a note by ID
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    try:
        note = Notes.query.get(note_id)
        if note:
            data = request.get_json()
            if 'title' not in data or 'content' not in data:
                return jsonify({'error': 'Title and content are required'}), 400
            note.title = data['title']
            note.content = data['content']
            db.session.commit()
            return jsonify({'message': 'Note updated successfully'})
        else:
            return jsonify({'error': 'Note not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Endpoint for LangChain integration (Note Summarization)
@app.route('/notes/<int:note_id>/summarize', methods=['GET'])
def summarize_note(note_id):
    try:
        model = os.environ.get("MODEL_NAME")
        note = Notes.query.get(note_id)
        if note:
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name=model)
            texts = text_splitter.split_text(note.content)
            docs = [Document(page_content=t) for t in texts]
            llm = ChatOpenAI(temperature=0, openai_api_key=os.environ.get("OPENAI_API_KEY"), 
                             model_name=model)
            prompt_template = """Write a concise summary of the following:
            {text}:"""
            prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
            chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=True)
            summary = chain.run(docs)
            return jsonify({'message': summary})
        else:
            return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)