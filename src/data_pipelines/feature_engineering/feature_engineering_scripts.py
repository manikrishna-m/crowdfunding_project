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
            ('categorical', Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder())
            ]), categorical_columns)
        ])

    transformed_data = pd.DataFrame(preprocessor.fit_transform(data))
    transformed_data.to_csv('data/processed/output_data.csv', index=False)
    logging.info("Data transformation completed successfully.")
except Exception as e:
    logging.exception("Data transformation failed.")
    raise CustomException(e, sys)
