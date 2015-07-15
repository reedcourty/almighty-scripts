@echo off

SET PORTABLE_PY34="d:\System\Programs\Python\App\Python 3.4.1 64bit\python.exe"
SET CURRENT_DIR=%CD%

py -3 %CURRENT_DIR%/ap_logger.py
if ERRORLEVEL 1 %PORTABLE_PY34% %CURRENT_DIR%/ap_logger.py
