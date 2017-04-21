@echo off
cd %~dp0/HealthNet
del db.sqlite3

FOR /d /r . %%d IN (migrations) DO @IF EXIST "%%d" rd /s /q "%%d"

setlocal enabledelayedexpansion

echo running checks...
set checker=Requires:
for /f %%i in ('pip show django-calendarium') do set str1="%%i"
::echo cal: %str1%
for /f %%i in ('pip show pytz') do set str2="%%i"
::echo pytz: %str2%

call :strLen strlen1 str1
call :strLen strlen2 str2

::if not "x!str1:%checker%=!"=="x%str1%" (
if %strlen1% == 0 (
	echo django-calendarium not found, installing....
	pip install django-calendarium --user
) else (
	echo django-calendarium found.
)
::if not "x!str2:%checker%=!"=="x%str2%" (
if %strlen2% == 0 (
	echo pytz not found, installing....
	pip install pytz --user
) else (
	echo pytz found.
)

endlocal

WHERE python3
IF %ERRORLEVEL% == 0 (
	echo using python3 command...
	python3 manage.py makemigrations core appointments messaging sysstats prescriptions transfer testResults calendarium
	python3 manage.py migrate
	python3 manage.py loaddata db.json 
) ELSE (
	echo using python command...
	python manage.py makemigrations core appointments messaging sysstats prescriptions transfer testResults calendarium
	python manage.py migrate
	python manage.py loaddata db.json
)
echo Done!

:strlen <resultVar> <stringVar>
(   
    setlocal EnableDelayedExpansion
    set "s=!%~2!#"
    set "len=0"
    for %%P in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
        if "!s:~%%P,1!" NEQ "" ( 
            set /a "len+=%%P"
            set "s=!s:~%%P!"
        )
    )
)
( 
    endlocal
    set "%~1=%len%"
    exit /b
)