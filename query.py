import sqlalchemy
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import func

from config.config import DATABASE_URI
from src.utils.models import XGBoostPredictionTable, LinearRegressionPredictionTable

# Create the SQLAlchemy engine and connect to the database
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Query for rows with NULL scores and NULL predictions or NULL fid in XGBoostPredictionTable
xgboost_rows = session.query(XGBoostPredictionTable).filter(
    or_(
        and_(
            XGBoostPredictionTable.predictions.is_(None)
        ),
        XGBoostPredictionTable.fid.is_(None)
    )
).all()

# Query for rows with NULL scores and NULL predictions or NULL fid in LinearRegressionPredictionTable
linear_regression_rows = session.query(LinearRegressionPredictionTable).filter(
    or_(
        and_(
            LinearRegressionPredictionTable.predictions.is_(None)
        ),
        LinearRegressionPredictionTable.fid.is_(None)
    )
).all()

# Print the rows with NULL scores and NULL predictions or NULL fid for each table
print("XGBoostPredictionTable - Rows with NULL predictions or NULL fid:")
for row in xgboost_rows:
    print(f"ID: {row.id}, FID: {row.fid}")

print("\nLinearRegressionPredictionTable - Rows with NULL predictions or NULL fid:")
for row in linear_regression_rows:
    print(f"ID: {row.id}, FID: {row.fid}")

# Query for count of rows with NULL scores in XGBoostPredictionTable
xgboost_count = session.query(func.count(XGBoostPredictionTable.id)).filter(XGBoostPredictionTable.score.is_(None)).scalar()

# Query for count of rows with NULL scores in LinearRegressionPredictionTable
linear_regression_count = session.query(func.count(LinearRegressionPredictionTable.id)).filter(LinearRegressionPredictionTable.score.is_(None)).scalar()

print(f"Number of rows with NULL scores in XGBoostPredictionTable: {xgboost_count}")
print(f"Number of rows with NULL scores in LinearRegressionPredictionTable: {linear_regression_count}")

# Query for total row count in XGBoostPredictionTable
xgboost_total_count = session.query(func.count(XGBoostPredictionTable.id)).scalar()

# Query for total row count in LinearRegressionPredictionTable
linear_regression_total_count = session.query(func.count(LinearRegressionPredictionTable.id)).scalar()

print(f"Total number of rows in XGBoostPredictionTable: {xgboost_total_count}")
print(f"Total number of rows in LinearRegressionPredictionTable: {linear_regression_total_count}")

# Close the session
session.close()
