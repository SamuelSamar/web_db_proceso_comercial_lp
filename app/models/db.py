from sqlalchemy import create_engine
from flask import current_app

def get_engine():
    engine = create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"])
    return engine