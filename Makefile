venv:
	python3 -m venv venv
	source venv/bin/activate && pip3 install -r requirements.txt

run:
	source venv/bin/activate && python3 main.py
