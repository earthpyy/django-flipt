start:
	docker-compose up -d django

lint:
	docker-compose exec django pylint flipt

test:
	docker-compose exec django pytest

build:
	docker-compose exec django poetry build
