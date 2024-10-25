runserver:
	python manage.py runserver

build-docker:
	docker build -t skin-classifier .

run-docker:
	docker run --name skin-classifier-container -p 8000:8000 skin-classifier
