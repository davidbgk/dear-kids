# https://suva.sh/posts/well-documented-makefiles/

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install:  ## Install project dependencies
	pip install -e .

dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

check:  ## Run code checkers
	black . --quiet
	flake8
	mypy dearkids
	isort --quiet

test:  ## Run tests
	pytest --ff --disable-warnings -x --quiet

run:  ## Run local server
	dearkids

prod:  ## Run gunicorn server
	gunicorn dearkids.__main__:app --worker-class roll.worker.Worker
