@echo off
cd /d "c:\blipping grounds\alx\alx-backend-python"
call .venv\Scripts\activate.bat
cd Django-Middleware-0x03
python manage.py runserver --settings=temp_settings 8000
pause