import arcpy
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Toolbox(object):
    def __init__(self):
        self.label = "My Simple CSV + GeoJSON Toolbox"
        self.alias = "my_simple_toolbox"
        self.tools = [CSVGeoJSONTool]


class CSVGeoJSONTool(object):
    def __init__(self):
        self.label = "Join CSV to GeoJSON and Plot"
        self.description = "Simple version with automatic workspace handling."
        self.canRunInBackground = False

    def getParameterInfo(self):

        in_csv = arcpy.Parameter(
            displayName="Input CSV file",
            name="in_csv",
            datatype="File",
            parameterType="Required",
            direction="Input"
        )
        in_csv.filter.list = ["csv"]

        in_geojson = arcpy.Parameter(
            displayName="Input GeoJSON file",
            name="in_geojson",
            datatype="File",
            parameterType="Required",
            direction="Input"
        )
        in_geojson.filter.list = ["json", "geojson"]

        out_workspace = arcpy.Parameter(
            displayName="Output workspace (File GDB or folder)",
            name="out_workspace",
            datatype="Workspace",
            parameterType="Required",
            direction="Input"
        )

        join_field = arcpy.Parameter(
            displayName="Join field name (exists in both CSV and GeoJSON attributes)",
            name="join_field",
            datatype="String",
            parameterType="Required",
            direction="Input"
        )

        numeric_field = arcpy.Parameter(
            displayName="Numeric field name in CSV for plotting",
            name="numeric_field",
            datatype="String",
            parameterType="Required",
            direction="Input"
        )

        display_option = arcpy.Parameter(
            displayName="Display option for feature class (drop-down only)",
            name="display_option",
            datatype="String",
            parameterType="Required",
            direction="Input"
        )
        display_option.filter.list = ["Single symbol", "Graduated colors", "Unique values"]
        display_option.value = "Single symbol"

        out_png = arcpy.Parameter(
            displayName="Output graph PNG",
            name="out_png",
            datatype="File",
            parameterType="Required",
            direction="Output"
        )
        out_png.filter.list = ["png"]

        return [
            in_csv, in_geojson, out_workspace,
            join_field, numeric_field, display_option, out_png
        ]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return


    def execute(self, parameters, messages):


        in_csv = parameters[0].valueAsText
        in_geojson = parameters[1].valueAsText
        out_workspace = parameters[2].valueAsText
        join_field = parameters[3].valueAsText
        numeric_field = parameters[4].valueAsText
        display_option = parameters[5].valueAsText
        out_png = parameters[6].valueAsText


        arcpy.env.workspace = out_workspace
        arcpy.env.overwriteOutput = True

        ws_desc = arcpy.Describe(out_workspace)
        ws_type = ws_desc.workspaceType  

        geojson_name = os.path.splitext(os.path.basename(in_geojson))[0]
        csv_name = os.path.splitext(os.path.basename(in_csv))[0]

        if ws_type == "FileSystem":
            fc_name = geojson_name + "_fc.shp"
            csv_table = os.path.join(out_workspace, csv_name + "_tbl.dbf")
        else:
            fc_name = geojson_name + "_fc"
            csv_table = os.path.join(out_workspace, csv_name + "_tbl")

        fc_path = os.path.join(out_workspace, fc_name)

        if arcpy.Exists(fc_path):
            arcpy.management.Delete(fc_path)
        if arcpy.Exists(csv_table):
            arcpy.management.Delete(csv_table)


        messages.addMessage("Converting GeoJSON to feature class...")
        arcpy.conversion.JSONToFeatures(in_geojson, fc_path)

        messages.addMessage("Copying CSV to table...")
        arcpy.management.CopyRows(in_csv, csv_table)

        layer_name = fc_name + "_lyr"
        arcpy.management.MakeFeatureLayer(fc_path, layer_name)
        arcpy.management.AddJoin(layer_name, join_field, csv_table, join_field)

        messages.addMessage("Display option selected: " + display_option)

        x_list = []
        y_list = []

        messages.addMessage("Reading data from CSV for plotting...")

        try:
            with arcpy.da.SearchCursor(csv_table, [join_field, numeric_field]) as cursor:
                for row in cursor:
                    if row[0] is None or row[1] is None:
                        continue
                        
                    raw_val = str(row[1])
                    clean_val = raw_val.replace("%", "").strip()
                    
                    try:
                        val_float = float(clean_val)
                        x_list.append(str(row[0]))
                        y_list.append(val_float)
                    except ValueError:
                        messages.addWarning("Skipping value '{}' - unable to convert to float.".format(raw_val))
                        continue
        except Exception as e:
            messages.addErrorMessage("Error reading data for plotting: " + str(e))
            return

        if not x_list: 
            messages.addWarning("No valid data found for plotting. Exiting tool.")
            return

        max_n = min(20, len(x_list))
        plot_x = x_list[:max_n]
        plot_y = y_list[:max_n]
        
        plt.figure(figsize=(10, 5))

        if display_option == "Graduated colors":
            messages.addMessage("Applying Graduated colors style to plot.")
            
            cmap = plt.cm.viridis 
            if max(plot_y) == min(plot_y):
                norm_y = [0.5] * len(plot_y) 
            else:
                norm = plt.Normalize(min(plot_y), max(plot_y))
                norm_y = norm(plot_y)
            bar_colors = cmap(norm_y)
            
            plt.bar(plot_x, plot_y, color=bar_colors) 

        elif display_option == "Unique values":
            messages.addMessage("Applying Unique values style (Categorical colors) to plot.")
            
            cmap_categorical = plt.cm.get_cmap('tab20')
            bar_colors = [cmap_categorical(i % 20) for i in range(len(plot_x))] 
            
            plt.bar(plot_x, plot_y, color=bar_colors)
            
        else: 
            messages.addMessage("Applying Single symbol style to plot.")
            plt.bar(plot_x, plot_y, color='#0077B6')

        plt.xticks(rotation=90)
        plt.xlabel(join_field)
        plt.ylabel(numeric_field)
        plt.title(f'{numeric_field} Distribution ({display_option})') 
        plt.tight_layout()
        plt.savefig(out_png, dpi=300)
        plt.close()

        messages.addMessage("Graph saved to: " + out_png)
