from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

# Define the Note model
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)