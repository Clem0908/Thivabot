install:
	chmod +x ./configure
	./configure
run:
	./venv/bin/python main.py --debug false
run-debug:
	./venv/bin/python main.py --debug true
