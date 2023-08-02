import sys
import os

# Get the absolute path to the parent directory of src (which contains config package)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

# Import from the correct package
from config.config import DATABASE_URI
from sqlalchemy import create_engine
from src.utils.models import Base

if __name__ == "__main__":
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
