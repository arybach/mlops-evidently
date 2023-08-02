from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LinearRegressionPredictionTable(Base):
    """Table for storing features with corresponding predictions for Linear Regression model."""

    __tablename__ = 'linear_regression_prediction'  
    id = Column(Integer, primary_key=True, autoincrement=True)
    fid = Column(String)

    # Numerical features
    fat = Column(Float)
    saturatedFat = Column(Float)
    transFat = Column(Float)
    cholesterol = Column(Float)
    sodium = Column(Float)
    carbohydrates = Column(Float)
    fiber = Column(Float)
    sugars = Column(Float)
    protein = Column(Float)
    calcium = Column(Float)
    iron = Column(Float)
    potassium = Column(Float)
    calories = Column(Float)

    score = Column(Float)
    predictions = Column(Float)


class XGBoostPredictionTable(Base):
    """Table for storing features with corresponding predictions for XGBoost model."""

    __tablename__ = 'xgboost_prediction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fid = Column(String)

    # Numerical features
    fat = Column(Float)
    saturatedFat = Column(Float)
    transFat = Column(Float)
    cholesterol = Column(Float)
    sodium = Column(Float)
    carbohydrates = Column(Float)
    fiber = Column(Float)
    sugars = Column(Float)
    protein = Column(Float)
    calcium = Column(Float)
    iron = Column(Float)
    potassium = Column(Float)
    calories = Column(Float)

    score = Column(Float)
    predictions = Column(Float)
