# Xurpas Data Quality Report

## How to Use
- Load the data to be analyzed (so far only csv files supported)
- Import the DataReport class
- Save the report to html File

#### Sample Usage
```python
from xurpas_data_quality import DataReport
a = DataReport("test_reports/manhour_utilization_summary.csv")
a.to_file("Manhour Utilization Summary", "test_reports/test.html")
```