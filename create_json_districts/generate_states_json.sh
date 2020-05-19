#!/bin/bash
minsize=220
wget https://www2.census.gov/geo/tiger/TIGER2019/CD/tl_2019_us_cd116.zip
rest="tl_2019_us_cd116.zip"
unzip $rest

ogr2ogr -f GeoJSON -t_srs crs:84 districts.json ${rest%.zip}.shp
mv districts.json info/
for i in {1..100}
do
	cat info/header.txt >> $i.txt
	grep '"STATEFP": "'$i'"' info/districts.json >> $i.txt
	truncate -s-2 $i.txt
	cat info/footer.txt >> $i.txt

	actualsize=$(wc -c < $i".txt")

	if (($actualsize > $minsize));
	then
		echo $i valid
		cat $i.txt >> $i.json

	else
		echo $i "not valid"
	fi
	rm $i.txt
		 
done
