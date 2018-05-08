REM Build resource files

start "uic" /B pyuic5 -xo src\ui\mainwindow.py ui\mainwindow.ui
start "rcc" /B pyrcc5 -o resources_rc.py resources.qrc
