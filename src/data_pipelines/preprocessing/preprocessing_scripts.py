import pandas as pd
import numpy as np
import pickle
import sys

from src.logger import logging
from src.exception import CustomException

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVR

from src.exception import CustomException

def preprocess_data(file_path):
    try:
        logging.info("Reading data from CSV...")
        data = pd.read_csv(file_path)

        numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_columns = data.select_dtypes(include=['object']).columns.tolist()

        preprocessor = ColumnTransformer(
            transformers=[
                ('numeric', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]), numeric_columns),
                ('categorical', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder()),
                    ('scaler', StandardScaler())
                ]), categorical_columns)
            ])

        X = data.drop('math_score', axis=1)
        y = data['math_score']

        logging.info("Splitting data into train and test sets...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        logging.info("Applying data transformation on train and test sets...")
        X_train = preprocessor.fit_transform(X_train)
        X_test = preprocessor.transform(X_test)

        X_train = np.c_[X_train, np.array(y_train)]
        X_test = np.c_[X_test, np.array(y_test)]

        with open('data/processed/preprocessor.pkl', 'wb') as f:
            pickle.dump(preprocessor, f)

        logging.info("Data transformation completed successfully.")
        return preprocessor, X_train, X_test, y_train, y_test

    except Exception as e:
        logging.exception("Data transformation or model training failed.")
        raise CustomException(e, sys)

# Usage example:
preprocessor, X_train, X_test, y_train, y_test = preprocess_data('data/processed/output_data.csv')
