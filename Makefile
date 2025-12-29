install:
	chmod +x ./configure
	./configure
run:
	./venv/bin/python main.py debug=False
run-debug:
	./venv/bin/python main.py debug=True
