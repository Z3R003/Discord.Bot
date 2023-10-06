@echo off
echo Installing Python libraries...
pip install -r requirements.txt 

echo Creating start.bat...
echo python main.py > start.bat

echo Installation completed successfully!

echo Deleting install.bat...
del install.bat
