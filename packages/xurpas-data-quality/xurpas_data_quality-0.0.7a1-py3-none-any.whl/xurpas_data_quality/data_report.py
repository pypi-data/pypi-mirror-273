import os
import warnings
from pathlib import Path

import pandas as pd

from xurpas_data_quality.render.renderer import HTMLBase
from xurpas_data_quality.data.dataframe import load_dataframe, validate_dataframe
from xurpas_data_quality.data.describe import describe
from xurpas_data_quality.report import get_report


class DataReport:
    def __init__(self, file:str=None, df:pd.DataFrame=None, report_name:str="Data Report", file_path:str="report.html"):
        """
        Initializes the DataReport object
        Args
            file:        The path of the file you want to analyze. If empty, df parameter must exist.
                         Only supports .csv, .xlsx, .parquet, and .orc file formats
            df:          Pandas DataFrame object of data to be analyzed, If using df, file must be empty.
            report_name: Name of the report. Defaults to 'Data Report'
            file_path:   Path/ directory of where the report is to be saved
        """

        self.report_name = report_name

        def has_extension(file_path:str):
            return os.path.splitext(file_path)[1] != '' 
        if has_extension(file_path):
            self.save_path = file_path
        else:
            self.save_path = '/'.join([file_path,"report.html"])
            warnings.warn("File name not provided, saving as {file_path}/report.html")
            
        if file is not None and df is None:
            self.df = load_dataframe(df)
        elif file is None and df is not None:
            self.df = df
        elif file is not None and df is not None:
            raise KeyError("Only 'file' or 'df' should be used one at a time!")
        elif file is None and df is None:
            raise ValueError("Please provide your data in 'file' or 'df' parameters!")
        
    def describe_dataframe(self):
        self.description = describe(self.df)

    def get_data_quality_report(self, name=None):
        self.describe_dataframe()
        report = get_report(self.description, name=name)
        return report.render()
    
    def to_file(self, report_name:str=None, file_name:str="report.html"):
        output = Path(self.save_path)
        print(f"saving as {self.save_path}")
        output.write_text(self.get_data_quality_report(self.report_name), encoding='utf-8')
        print(f"saved!")