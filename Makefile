run:
	python3 -m app.server

format:
	black app

lint:
	flake8 app
