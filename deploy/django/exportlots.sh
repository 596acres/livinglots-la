#!/bin/bash

source $HOME/.bashrc
source $HOME/.virtualenvs/laopenacres/bin/activate
GEOJSON_FILE=$DOWNLOAD_DATA_DIR/laopenacres_lots_$(date +%Y%m%d).geojson
SHP_FILE=$DOWNLOAD_DATA_DIR/laopenacres_lots_$(date +%Y%m%d).shp
django-admin.py exportlots > $GEOJSON_FILE
ogr2ogr -f "ESRI Shapefile" $SHP_FILE $GEOJSON_FILE
