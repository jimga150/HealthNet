@echo off
cd %~dp0/HealthNet
del db.sqlite3
cd ..

FOR /d /r . %%d IN (migrations*) DO @IF EXIST "%%d" rd /s /q "%%d"

WHERE python3
IF %ERRORLEVEL% == 0 (
	echo using python3 command...
	python3 -m pip install -qr requirements.txt --user
	cd %~dp0/HealthNet
	python3 manage.py makemigrations core appointments messaging sysstats prescriptions transfer testResults calendarium
	python3 manage.py migrate
	python3 manage.py loaddata db.json 
) ELSE (
	echo using python command...
	python -m pip install -qr requirements.txt --user
	cd %~dp0/HealthNet
	python manage.py makemigrations core appointments messaging sysstats prescriptions transfer testResults calendarium
	python manage.py migrate
	python manage.py loaddata db.json
)
echo Done!