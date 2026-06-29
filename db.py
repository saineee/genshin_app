from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# load variables from .env into environment
load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
Base = declarative_base()
Session = sessionmaker(bind=engine)
