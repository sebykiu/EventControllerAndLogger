import pyproj

source_projection = pyproj.Proj("+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

target_projection = pyproj.Proj(init="epsg:4326")  # EPSG code for WGS84

utm_x = 692152.0894735109
utm_y = 5337384.6661008

lon, lat = pyproj.transform(source_projection, target_projection, utm_x, utm_y)

print("Longitude:", lon)
print("Latitude:", lat)
