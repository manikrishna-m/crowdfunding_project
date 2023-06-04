import pandas as pd
import sys

from src.logger import logging
from src.exception import CustomException

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

data = pd.read_csv('data/processed/output_data.csv')

numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_columns = data.select_dtypes(include=['object']).columns.tolist()

try:
    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', SimpleImputer(strategy='median'), numeric_columns),
            ('categorical', SimpleImputer(strategy='most_frequent'), categorical_columns)
        ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('encoder', OneHotEncoder())
    ])

    transformed_data = pd.DataFrame(pipeline.fit_transform(data))
    
    logging.info("Data transformation completed successfully.")
except Exception as e:
    logging.exception("Data transformation failed.")
    raise CustomException(e, sys)