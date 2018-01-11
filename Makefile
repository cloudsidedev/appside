all:
	rm -rf appflow.egg-info build dist;
	python3 setup.py  sdist;
	pip3 uninstall appflow;
	pip3 install dist/appflow-1.*..tar.gz;
clean:
	rm -rf appflow.egg-info build dist;

build:
	python3 setup.py  sdist;

install:
	pip3 install dist/appflow-1.*.tar.gz

reinstall:
	pip3 uninstall appflow;
	pip3 install dist/appflow-1.*.tar.gz;

uninstall:
	pip3 uninstall appflow;

sign:
	gpg --detach-sign -a dist/appflow-1.*.tar.gz

upload:
	twine upload dist/appflow-1.*.tar.gz dist/appflow-1.*.tar.gz.asc


