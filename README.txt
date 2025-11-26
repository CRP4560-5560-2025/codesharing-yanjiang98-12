Author
Yan Jiang

Date Created
November/25/2025

Purpose of the Code

This project provides an ArcGIS Python Toolbox designed to integrate statistical CSV data with geographic boundary data stored in GeoJSON format.
The toolbox performs three primary operations:

Converts a GeoJSON file into an ArcGIS Feature Class, making the geographic boundaries directly usable in ArcGIS.

Imports a CSV file as an ArcGIS table, enabling attribute-based operations.

Joins the CSV table to the Feature Class using user-specified join fields from each dataset.

After the join operation, the tool uses Matplotlib to generate a bar chart based on a numeric field selected from the CSV.
The overall purpose is to combine spatial information with attribute information and to provide an additional statistical visualization of the data.

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

Output workspace folder

CSV join field name (NAME)

GeoJSON join field name (PctUnder5)

Numeric field for plotting

Output PNG path and naming the file

Execute the Tool

Click Run.
