#!/bin/sh

if type -p pyuic4 > /dev/null; then
    PYUIC=pyuic4
elif type -p pyuic > /dev/null; then
    PYUIC=pyuic
elif [ -f /usr/share/pyshared/PyQt4/uic/pyuic.py ]; then
    PYUIC="python /usr/share/pyshared/PyQt4/uic/pyuic.py"
elif [ -x /opt/local/Library/Frameworks/Python.framework/Versions/2.5/bin/pyuic4 ]; then 
    PYUIC=/opt/local/Library/Frameworks/Python.framework/Versions/2.5/bin/pyuic4
else
    echo "error: cannot find pyuic"
    exit 1
fi

echo "using \"$PYUIC\""
	
$PYUIC MainWindow.ui > Ui_MainWindow.py
