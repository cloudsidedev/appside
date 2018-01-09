all:
	rm -rf appflow.egg-info build dist;
	python3 setup.py  sdist bdist;
	pip3 uninstall appflow;
	pip3 install dist/appflow-1.0.0.tar.gz;

