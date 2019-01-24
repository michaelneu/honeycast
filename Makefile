.PHONY: venv run image rmi run_image

venv:
	python3 -m venv venv
	source venv/bin/activate && pip3 install -r requirements.txt

run:
	source venv/bin/activate && python3 main.py

image:
	docker build -t honeycast_dev .

rmi:
	docker rmi honeycast_dev

run_image:
	docker run \
		--rm \
		-it \
		-p 8008:8008 \
		-p 8009:8009 \
		honeycast_dev
