import pandas as pd

from pathlib import Path

from xurpas_data_quality.render.renderer import HTMLBase
from xurpas_data_quality.data.dataframe import load_dataframe, validate_dataframe
from xurpas_data_quality.data.describe import describe
from xurpas_data_quality.report import get_report


class DataReport:
    def __init__(self, df:str):
        if df is None:
            raise ValueError("there must be an input!")
        self.df = load_dataframe(df)
        
    def describe_dataframe(self):
        self.description = describe(self.df)

    def get_data_quality_report(self, name=None):
        self.describe_dataframe()
        report = get_report(self.description, name=name)
        return report.render()
    
    def to_file(self, report_name:str=None, file_name:str="report.html"):
        output = Path(file_name)
        print(f"saving as {file_name}")
        output.write_text(self.get_data_quality_report(report_name), encoding='utf-8')
        print(f"saved!")