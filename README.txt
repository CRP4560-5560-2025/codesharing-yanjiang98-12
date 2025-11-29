Author
Yan Jiang

Date Created
November/25/2025

Purpose of the Code

This toolbox provides a simple workflow for joining Census CSV data with a GeoJSON file, converting the GeoJSON into a feature class, and visualizing numeric attributes through a basic matplotlib graph. It is designed to demonstrate file selection, workspace handling, field-based joining, and graphical output in ArcGIS Pro using a Python Toolbox.

Data Accessed

This toolbox uses two data sources:

Under5yearsPercentAGETotalpopulation.csv: Contains Census Tract–level statistics on the percentage of population under age five.

Under5yearsPercentAGETotalpopulation_MapLayer.json: GeoJSON file containing Census Tract geographic boundaries and attributes.

These two datasets are used together by performing an attribute join between a text field in the CSV  and the corresponding geographic identifier in the GeoJSON.

How to Run This Code Package

Open ArcGIS Pro.

Place the toolbox file and the data files inside the project folder.

Open the Catalog pane

Right-click Toolboxes → Add Toolbox

Select the toolbox file 

When running, enter the following inputs:

Input CSV file 

Input GeoJSON file 

Select the Output workspace folder

Join field name (input: NAME)

Numeric field name for plotting (input: PctUnder5)

Select Graduated colors as the Display option  

naming the Output PNG file and its path 

Run the Tool
