To generate the documentation:

mv ../appflow ../appflow.py
rm source/*rst
sphinx-apidoc -o ./source .. ../
make clean && make html
mv ../appflow.py ../appflow