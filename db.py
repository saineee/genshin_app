from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://paul:7285@127.0.0.1/genshindb")
Base = declarative_base()
Session = sessionmaker(bind=engine)