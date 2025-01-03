# Convex-Hull-Visualization-of-Cellular-Towers
This repository contains a Python program that processes a dataset of cellular towers and visualizes their locations on an interactive map. It also calculates the Convex Hull of the selected tower locations using the Graham Scan Algorithm and saves the details of the vertices and internal points to an Excel file.
Features
Interactive Map Visualization:

Displays cellular tower locations on an interactive map using the Folium library.
Highlights the convex hull boundary that encloses the selected points.
Convex Hull Calculation:

Implements the Graham Scan Algorithm to calculate the convex hull for a given set of geographic coordinates.
Efficiently identifies the outermost points (vertices) forming the convex hull.
Data Management:

Reads tower data (latitude, longitude, city name) from an Excel file.
Saves the convex hull vertices and inside points to a new Excel file, categorizing points as either "Vertex" or "Inside".
Performance Metrics:

Measures and prints the time taken to calculate the convex hull.
Customizable Parameters:

Number of towers to visualize (user-defined).
Adjustable coverage radius for towers (default: 5 km).
How It Works
User Input:

The user specifies the number of towers to include (1 to 2000).
The program reads the data from the provided Excel file containing tower information.
Data Processing:

Extracts tower locations and removes duplicates.
Computes the convex hull for the specified number of points.
Visualization:

Creates an interactive map centered at the average location of the selected towers.
Marks tower locations with tooltips showing the city names.
Draws a polygon representing the convex hull boundary.
Output:

Saves the interactive map as cellulartowersmap.html.
Exports an Excel file (convex_hull_and_inside_details.xlsx) containing:
Vertices of the convex hull.
Points inside the convex hull.
Key Functions
graham_scan(points):

Implements the Graham Scan Algorithm to calculate the convex hull for a set of points.
Returns the coordinates of the convex hull vertices.
create_map_with_towers(file_path, num_towers, coverage_radius=5):

Reads data from the Excel file.
Visualizes tower locations on a map with a convex hull overlay.
Saves the details of hull vertices and inside points to an Excel file.
