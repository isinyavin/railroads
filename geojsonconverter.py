import geopandas as gpd

geojson_path = 'dublinrails.geojson'
geojson_path2 = 'dublinstations.geojson'
gdf1 = gpd.read_file(geojson_path)
gdf2 = gpd.read_file(geojson_path2)


#gdf1['geometry'] = gdf1['geometry'].apply(lambda x: x.wkt)
#gdf2['geometry'] = gdf2['geometry'].apply(lambda x: x.wkt)

# Save to Feather
gdf1.to_feather('dublinrails.feather')
gdf2.to_feather('dublinstation.feather')
