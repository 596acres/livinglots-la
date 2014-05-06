#!/bin/bash

source $HOME/.bashrc
source $HOME/.virtualenvs/laopenacres/bin/activate

GEOJSON_FILE=lots_$(date +%Y%m%d).geojson
GEOJSON_LATEST_FILE=laopenacres_lots_latest.geojson
SHP_FILE_PREFIX=lots_$(date +%Y%m%d)
ZIP_FILE=lots_shp_$(date +%Y%m%d).zip
ZIP_LATEST_FILE=laopenacres_lots_latest_shp.zip

# Generate GeoJSON and Shapefile
cd $DOWNLOAD_DATA_DIR
django-admin.py exportlots > $GEOJSON_FILE
ogr2ogr -f "ESRI Shapefile" ${SHP_FILE_PREFIX}.shp $GEOJSON_FILE
zip $ZIP_FILE ${SHP_FILE_PREFIX}.{dbf,prj,shp,shx}

# Make latest
cp $GEOJSON_FILE $GEOJSON_LATEST_FILE
cp $ZIP_FILE $ZIP_LATEST_FILE
