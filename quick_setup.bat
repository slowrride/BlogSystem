@echo off
cd /d %~dp0

echo Deleting old database...
del db.sqlite3 2>nul

echo Generating migrations...
python manage.py makemigrations

echo Applying migrations...
python manage.py migrate

echo Done! Now run: python manage.py createsuperuser
pause
