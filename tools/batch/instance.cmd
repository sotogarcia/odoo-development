@echo off

GOTO %1

:CREATE

SET INSTANCES_PATH=D:\TRABAJO\ODOO\instances
SET OCB_SOURCE=D:\TRABAJO\ODOO\sources\OCB
SET TPL_SOURCE=D:\TRABAJO\ODOO\templates

mkdir %INSTANCES_PATH%\%2
mkdir %INSTANCES_PATH%\%2\addons
mkdir %INSTANCES_PATH%\%2\data_dir

copy "%TPL_SOURCE%\openerp-server.conf" "%INSTANCES_PATH%\%2"

FOR /D %%R IN ("%OCB_SOURCE%\addons\*") DO (
    MKLINK /D "%INSTANCES_PATH%\%2\addons\%%~nxR" "%OCB_SOURCE%\addons\%%~nxR"
)


MKLINK /D "%INSTANCES_PATH%\%2\debian" "%OCB_SOURCE%\debian"
MKLINK /D "%INSTANCES_PATH%\%2\doc" "%OCB_SOURCE%\doc"
MKLINK /D "%INSTANCES_PATH%\%2\openerp" "%OCB_SOURCE%\openerp"
MKLINK /D "%INSTANCES_PATH%\%2\setup" "%OCB_SOURCE%\setup"

MKLINK "%INSTANCES_PATH%\%2\.gitignore" "%OCB_SOURCE%\.gitignore"
MKLINK "%INSTANCES_PATH%\%2\.mailmap" "%OCB_SOURCE%\.mailmap"
MKLINK "%INSTANCES_PATH%\%2\.travis.yml" "%OCB_SOURCE%\.travis.yml"
MKLINK "%INSTANCES_PATH%\%2\CONTRIBUTING.md" "%OCB_SOURCE%\CONTRIBUTING.md"
MKLINK "%INSTANCES_PATH%\%2\LICENSE" "%OCB_SOURCE%\LICENSE"
MKLINK "%INSTANCES_PATH%\%2\Makefile" "%OCB_SOURCE%\Makefile"
MKLINK "%INSTANCES_PATH%\%2\MANIFEST.in" "%OCB_SOURCE%\MANIFEST.in"
MKLINK "%INSTANCES_PATH%\%2\odoo.py" "%OCB_SOURCE%\odoo.py"
MKLINK "%INSTANCES_PATH%\%2\openerp-gevent" "%OCB_SOURCE%\openerp-gevent"
MKLINK "%INSTANCES_PATH%\%2\openerp-server" "%OCB_SOURCE%\openerp-server"
MKLINK "%INSTANCES_PATH%\%2\openerp-wsgi.py" "%OCB_SOURCE%\openerp-wsgi.py"
MKLINK "%INSTANCES_PATH%\%2\README.md" "%OCB_SOURCE%\README.md"
MKLINK "%INSTANCES_PATH%\%2\requirements.txt" "%OCB_SOURCE%\requirements.txt"
MKLINK "%INSTANCES_PATH%\%2\setup.cfg" "%OCB_SOURCE%\setup.cfg"
MKLINK "%INSTANCES_PATH%\%2\setup.py" "%OCB_SOURCE%\setup.py"

GOTO FIN

:REMOVE

:FIN
SET INSTANCES_PATH=
SET OCB_SOURCE=
SET TPL_SOURCE=