@echo off

GOTO %1

:RUN
    TASKKILL /F /IM PYTHON.EXE
    
    IF [%3] == [] (
    	PYTHON.EXE "D:\TRABAJO\ODOO\instances\%2\ODOO.PY"
    ) ELSE (
    	PYTHON.EXE "D:\TRABAJO\ODOO\instances\%2\ODOO.PY" --update=%3
    )
    
    GOTO FIN

:TEST
    TASKKILL /F /IM PYTHON.EXE
    
    PYTHON.EXE "D:\TRABAJO\ODOO\instances\%2\ODOO.PY" --init=%3 --update=%3 --test-enable --log-level=test --database=%4
    
    GOTO FIN

:FIN