import pandas as pd
import sys

from src.exception import CustomException
from src.logger import logging

class DataInjector:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
    
    def inject_data(self):
        try:
            data = pd.read_csv(self.input_file)
            data.to_csv(self.output_file, index=False)         
            logging.info("Data injection completed successfully.")
        except Exception as e:
            
            logging.exception("Data injection failed.")
            raise CustomException(e, sys)

input_file = 'data/raw/stud.csv'
output_file = 'data/processed/output_data.csv'
data_injector = DataInjector(input_file, output_file)
data_injector.inject_data()
