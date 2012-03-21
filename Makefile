all: Ui_MainWindow.py
doc: report

Ui_MainWindow.py: MainWindow.ui
	./gen.sh

run: Ui_MainWindow.py
	./PyFauxFur.py

report:
	cd $@ && rubber --pdf report.tex

test: Ui_MainWindow.py
	./test_images.sh

.PHONY: all doc run report test
