#!/bin/bash

source $HOME/.bashrc
source $HOME/.virtualenvs/laopenacres/bin/activate

GEOJSON_FILE=laopenacres_lots_$(date +%Y%m%d).geojson
SHP_FILE_PREFIX=laopenacres_lots_$(date +%Y%m%d)
ZIP_FILE=laopenacres_lots_$(date +%Y%m%d).zip

cd $DOWNLOAD_DATA_DIR
django-admin.py exportlots > $GEOJSON_FILE
ogr2ogr -f "ESRI Shapefile" ${SHP_FILE_PREFIX}.shp $GEOJSON_FILE
zip $ZIP_FILE ${SHP_FILE_PREFIX}.{dbf,prj,shp,shx}
