#!/bin/bash

pip_packages=“$(pip freeze)”
if [[ ${pip_packages} == *django-calendarium* ]]; then
	echo django-calendarium found.
else
  	echo django-calendarium not found, installing....
	pip install django-calendarium
fi
if [[ ${pip_packages} == *pytz* ]]; then
	echo pytz found.
else
  	echo pytz not found, installing....
	pip install pytz
fi

echo Nuking database..
cd HealthNet/;
sudo rm -rf db.sqlite3 */migrations/ &&
echo Nuked.

if type python3 >/dev/null 2>&1; then
	echo Using command python3....
	python3 manage.py makemigrations core appointments messaging sysstats prescriptions transfer testResults calendarium&&
	python3 manage.py migrate &&
	python3 manage.py loaddata db.json
else
	echo Using command python....
	python manage.py makemigrations core appointments messaging sysstats prescriptions transfer testResults calendarium&&
	python manage.py migrate &&
	python manage.py loaddata db.json
fi


