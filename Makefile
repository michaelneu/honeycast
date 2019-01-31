.PHONY: venv run image rmi run_image

venv:
	python3 -m venv venv
	source venv/bin/activate && pip3 install -r requirements.txt

run:
	source venv/bin/activate && python3 main.py

certificates:
	echo "\n\n\n\n\n\n" | openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem

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
		-v `pwd`/honeycast.log:/app/honeycast.log \
		honeycast_dev
