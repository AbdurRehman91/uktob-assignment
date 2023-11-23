import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
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
    notes = Notes.query.all()
    notes_list = [{'id': note.id, 'title': note.title, 'content': note.content} for note in notes]
    return jsonify({'notes': notes_list})

# API Endpoint for getting a specific note by ID
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    try:
        note = Notes.query.get(note_id)
        if note:
            return jsonify({'id': note.id, 'title': note.title, 'content': note.content})
        return jsonify({'error': 'Note not found'}), 404
    except Exception as e:

        return jsonify({'error': str(e)}), 500

# API Endpoint for deleting a note by ID
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        note = Notes.query.get(note_id)
        if note:
            db.session.delete(note)
            db.session.commit()
            return jsonify({'message': 'Note deleted successfully'})
        else:
            return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Endpoint for LangChain integration (Note Summarization)
@app.route('/notes/<int:note_id>/summarize', methods=['GET'])
def summarize_note(note_id):
    note = Notes.query.get_or_404(note_id)
    langchain_api_url = 'https://api.openai.com/v1/langchain/summarize'
    langchain_api_key = 'YOUR_LANGCHAIN_API_KEY'  # Replace with your actual LangChain API key

    headers = {
        'Authorization': f'Bearer {langchain_api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        'text': note.content,
    }

    response = requests.post(langchain_api_url, json=data, headers=headers)

    if response.status_code == 200:
        summary = response.json()['summary']
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'Failed to generate summary'}), 500

if __name__ == '__main__':
    app.run(debug=True)