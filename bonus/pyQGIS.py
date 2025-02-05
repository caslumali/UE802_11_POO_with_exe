from qgis.core import QgsVectorLayer, QgsProject, QgsRendererCategory, QgsCategorizedSymbolRenderer, QgsSymbol
from PyQt5.QtGui import QColor
import os

# Getting the current QGIS project file path
project = QgsProject.instance()
project_path = project.fileName()

# If the project is saved, use its directory as the base for the relative path
if project_path:
    base_dir = os.path.dirname(project_path)
    geojson_relative_path = os.path.join(
        base_dir, '..', 'outputs', 'proprietaires.geojson')
else:
    # If the project is not saved, prompt the user or set a default path
    print("Project is not saved. Please save the project or specify a path manually.")
    geojson_relative_path = '../outputs/proprietaires.geojson'

# Load the GeoJSON layer
layer = QgsVectorLayer(geojson_relative_path, "Propriétaires", "ogr")
if not layer.isValid():
    print("Error loading the layer.")
else:
    # Add the layer to the QGIS project
    QgsProject.instance().addMapLayer(layer)

    # Check if the 'Propriétaires' column exists to avoid errors
    if 'Propriétaires' in layer.fields().names():
        # Collect unique values from the 'Propriétaires' column
        unique_owners = set()
        for feature in layer.getFeatures():
            owner = feature['Propriétaires']
            if owner:  # Ensure the string is not empty
                unique_owners.add(owner)

        # Create symbol categories for each unique value of 'Propriétaires'
        categories = []
        for i, owner in enumerate(unique_owners):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            # Dynamically set the symbol color for visual diversity
            symbol.setColor(
                QColor.fromHsv(
                    (360 * i / len(unique_owners)) %
                    360, 255, 255))
            category = QgsRendererCategory(owner, symbol, owner)
            categories.append(category)

        # Apply the categorized renderer to the layer
        renderer = QgsCategorizedSymbolRenderer('Propriétaires', categories)
        layer.setRenderer(renderer)

        # Update the layer display
        layer.triggerRepaint()
    else:
        print("'Propriétaires' column not found in the layer.")
