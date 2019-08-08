# https://suva.sh/posts/well-documented-makefiles/

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

check:  ## Run code checkers
	black .
	flake8
	mypy .
	isort

test:  ## Run tests
	pytest --ff --disable-warnings -x

run:  ## Run local server
	python dearkids

prod:  ## Run gunicorn server
	gunicorn dearkids.__main__:app --worker-class roll.worker.Worker
