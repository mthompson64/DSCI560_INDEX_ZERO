# INDEX ZERO
### Team Members:
Cameron Yap, Emily Christiansen, Madeleine Thompson, Stefan Lin

### To Run App:
```
cd <this_directory>
python init.py
```
You should then see something similar to the following on the command line:
```
Dash is running on http://127.0.0.1:8050/
```
Copy and paste the url to your browser to run the app locally and debug.

### Requirements:
```
pip install dash
pip install dash_bootstrap_components
pip install plotly
pip install pandas
```

### Repo Structure
```
- apps
    |-- __init__.py
    |-- home.py
    |-- ui.py
- assets
    |-- 
- data
    |-- agg_stats.csv
    |-- cleaned_data.csv
- .gitignore
- app_copy.py (ignore this file, this is a copy of the original one-page app)
- app.py
- dashboard_layout.ipynb
- index.py
- README.md
```

### Resources:
- [Plotly Dash](https://dash.plotly.com/)
    - [Multi-page Support](https://dash.plotly.com/urls)
    - [Interactive Graphing](https://dash.plotly.com/interactive-graphing)
    - [dcc.Graph](https://dash.plotly.com/dash-core-components/graph)
- [Plotly](https://plotly.com/python/)
- [Dash Bootstrap Cheatsheet](https://dashcheatsheet.pythonanywhere.com/)
- [Dash for Beginners: Create Interactive Python Dashboards (Towards Data Science)](https://towardsdatascience.com/dash-for-beginners-create-interactive-python-dashboards-338bfcb6ffa4)
- [Beginner’s Guide to Building a Multi-Page App using Dash, Plotly and Bootstrap (Towards Data Science)](https://towardsdatascience.com/beginners-guide-to-building-a-multi-page-dashboard-using-dash-5d06dbfc7599)