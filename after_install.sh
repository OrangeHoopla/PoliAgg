#!/usr/bin/env bash

# Install libaries
test=$(pwd)
echo $test
sudo pip3 install django
sudo pip3 install django-filter
sudo yum install python3-devel
sudo pip3 install mysqlclient
sudo pip3 install mysql-connector-python==8.0.17
sudo pip3 install requests
sudo pip3 install bs4
sudo pip3 install python-twitter
#starting server
cd "${test}Poly_Map/"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
test=$(pwd)
echo $test
pwd