# Xurpas Data Quality Report

## How to Use
- Load the data to be analyzed (so far only csv files supported)
- Import the DataReport class
- Save the report to html File

## DataReport
Creates and saves to file the data report.

Args
    report_name: Name of the report eg. "Data Quality Report". Default: **"Data Report"**
    file_path: filepath and filename to save. Default: **"report.html"**

Returns
    HTML File of data quality Report

#### Sample Usage
```python
from xurpas_data_quality import DataReport
report = DataReport("test_reports/manhour_utilization_summary.csv")
report.to_file(report_name="Manhour Utilization Summary", file_path="test_reports/test.html")
```