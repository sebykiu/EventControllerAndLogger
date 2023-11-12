import pyproj

source_projection = pyproj.Proj("+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

target_projection = pyproj.Proj(init="epsg:4326")  # EPSG code for WGS84

# Coordinates in UTM
utm_x = 692152.0894735109
utm_y = 5337384.6661008

# Perform the coordinate transformation
lon, lat = pyproj.transform(source_projection, target_projection, utm_x, utm_y)

# The 'lon' and 'lat' variables now contain the longitude and latitude in WGS84.
print("Longitude:", lon)
print("Latitude:", lat)
