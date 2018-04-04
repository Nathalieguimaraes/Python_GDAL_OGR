#!C:/Python2713/python.exe -u 
# -*- coding: utf-8 -*-
from math import sqrt
from osgeo import ogr
import osgeo.ogr as ogr 
import osgeo.osr as osr
import os, sys
import csv

#Save in CSV file
f = open('C:/xampp/htdocs/sds/py_tests/proj/lat03.csv','w')
i = 0
f.write(str('latitude,longitude,x,y')+"\n")                
while (i<len(coords_lonX03)):   
    f.write(str(coords_latX03[i])+","+str(coords_lonX03[i])+","+str(increment_X03[i])+","+str(increment_Y03)+"\n")
    i = i + 1
f.close()              
          

#Open CSV file - Using dictionary reader to access by field name
reader = csv.DictReader(open('lat03.csv','rb'),
    delimiter = ',',
    lineterminator='\n',
    quoting = csv.QUOTE_NONE)
 
#Set up the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

#Create the data source
data_source = driver.CreateDataSource('lat03.shp')

#Create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

#Create the Layer
layer = data_source.CreateLayer('lat03', srs, ogr.wkbPoint)

#Add the fields
layer.CreateField(ogr.FieldDefn('latitude',ogr.OFTReal))
layer.CreateField(ogr.FieldDefn('longitude',ogr.OFTReal))
layer.CreateField(ogr.FieldDefn('x',ogr.OFTReal))
layer.CreateField(ogr.FieldDefn('y',ogr.OFTReal))

#Process the CSV file and add the attibutes to the shapefile
for row in reader:
    #create the feature
    feature = ogr.Feature(layer.GetLayerDefn())
    #Set the attributes from CSV file
    feature.SetField('Latitude', row['latitude']) 
    feature.SetField('Longitude', row['longitude'])
    feature.SetField('X', row['x'])                      
    feature.SetField('Y', row['y']) 

#Create the WKT for the feature using Python string formatting
wkt = 'POINT(%f %f)' % (float(row['longitude']), float(row['latitude']))

#Create the point from CSV
point = ogr.CreateGeometryFromWkt(wkt)

#Set the feature geometry using the point 
feature.SetGeometry(point)
#Create the feature in the Layer shp
layer.CreateFeature(feature)
#Deference the feature
feature = None 

#Save and close the data source
data_source = None