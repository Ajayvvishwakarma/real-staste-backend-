@echo off

echo Setting up 99Acres Backend API...

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete!
echo.
echo To start the development server:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Make sure MongoDB is running
echo 3. Run: python -m app
echo.
echo API Documentation will be available at: http://localhost:8000/docs

pause