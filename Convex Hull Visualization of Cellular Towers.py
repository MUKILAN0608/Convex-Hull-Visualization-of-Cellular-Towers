!pip install folium pandas scipy openpyxl
import folium
import numpy as np
import pandas as pd
import time

def graham_scan(points):
    
    points = sorted(points, key=lambda p: (p[1], p[0]))
    anchor = points[0]

 
    def polar_angle(p):
      
        y_span = p[1] - anchor[1]
        x_span = p[0] - anchor[0]
        return np.arctan2(y_span, x_span)

    def distance(p):
    
        y_span = p[1] - anchor[1]
        x_span = p[0] - anchor[0]
        return y_span ** 2 + x_span ** 2

    def det(p1, p2, p3):
      
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

 
    sorted_points = sorted(points[1:], key=lambda p: (polar_angle(p), -distance(p)))

    hull = [anchor, sorted_points[0]]
    for point in sorted_points[1:]:
      
        while len(hull) > 1 and det(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)

    return np.array(hull)

def create_map_with_towers(file_path, num_towers, coverage_radius=5):
    try:
       
        data1 = pd.read_excel(file_path, usecols=['latdec', 'londec', 'LocCity']).dropna()
        data = data1.drop_duplicates()

        
        points = data[['latdec', 'londec']].head(num_towers).to_numpy()
        
        
        avg_lat, avg_lon = np.mean(points, axis=0)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

        
        for _, row in data.head(num_towers).iterrows():
            folium.Marker(
                location=[row['latdec'], row['londec']],
                icon=folium.Icon(color='blue', icon='info-sign'),
                tooltip=row['LocCity']
            ).add_to(m)

        
        start_time = time.time()
        hull_points = graham_scan(points)
        end_time = time.time()

   
        folium.Polygon(
            locations=hull_points.tolist(),
            color='blue', weight=2, fill=True, fill_color='blue', fill_opacity=0.1
        ).add_to(m)

        print(f"Time to calculate convex hull: {end_time - start_time:.6f} seconds")

        
        hull_df = pd.DataFrame(hull_points, columns=['latdec', 'londec'])
        hull_df['LocCity'] = hull_df.apply(lambda row: data.loc[
            (data['latdec'] == row['latdec']) & (data['londec'] == row['londec']), 'LocCity'].values[0], axis=1)
        hull_df['Type'] = 'Vertex'  

       
        inside_points = []
        for i in range(len(points)):
            if not any(np.array_equal(points[i], hull_point) for hull_point in hull_points):
                inside_points.append(points[i])

        inside_df = pd.DataFrame(inside_points, columns=['latdec', 'londec'])
        inside_df['LocCity'] = inside_df.apply(lambda row: data.loc[
            (data['latdec'] == row['latdec']) & (data['londec'] == row['londec']), 'LocCity'].values[0], axis=1)
        inside_df['Type'] = 'Inside'  

       
        combined_df = pd.concat([hull_df, inside_df], ignore_index=True)

       
        combined_df = combined_df.drop_duplicates(subset=['latdec', 'londec'])

      
        combined_df.to_excel("convex_hull_and_inside_details.xlsx", index=False)
        print("Convex hull and inside details saved as 'convex_hull_and_inside_details.xlsx'.")

        return m

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
      
        N = int(input("Enter the number of towers (1-2000): "))
        if not (1 <= N <= 2000):
            raise ValueError("Please enter a positive integer between 1 and 2000.")
    except ValueError as ve:
        print(ve)
        exit(1)

  
    file_path = "C:\\Users\\Mukil\\Downloads\\Cellular Towers In USA.xlsx"
    map_result = create_map_with_towers(file_path, N)
    if map_result:
        map_result.save("cellulartowersmap.html")
        print("Map saved as 'cellulartowersmap.html'.")
