#!/bin/sh

# Merging all csvfiles inside of folders into one csv file.
# copy to the root of folders
#---------------


FOLDER=$1
#FOLDER=prediction

if [ -f $FOLDER/pred-1*.csv ];then
com=$(head -1 $FOLDER/pred-1-*.csv > $FOLDER/prediction.csv)
fi

for file in $(ls -1v $FOLDER/pred-*.csv )
do

#new_file=$(basename "$folder")
echo "================================================="

echo "reading " $file
tail -n +2 -q $file >> $FOLDER/prediction.csv
echo "================================================="

done



if [ -f $FOLDER/prediction.csv ];then
echo "creating zip file"
com=$(zip  $FOLDER/prediction.tar.gz $FOLDER/prediction.csv)
fi
