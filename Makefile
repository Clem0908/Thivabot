install:
	chmod +x ./configure
	./configure
run:
	./venv/bin/python main.py 2> stderr.log 1> stdout.log
