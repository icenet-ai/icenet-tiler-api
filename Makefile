.PHONY: build run dev run-dev remove-image

export TAG        ?= "dev"
export TILER_PORT ?= 8000
export DATA_PORT  ?= 8002
export WORKERS    ?= 12
export DOCKER_DATA_DIR="/app/mounted_vols/data"
IMAGE_NAME = "icenet-dashboard/plotly-dash-web-dashboard:$(TAG)"

build:
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Starting tile and static data servers with honcho (PORTS: $(TILER_PORT), $(DATA_PORT), WORKERS: $(WORKERS))"
	@honcho start

dev:
	@echo "Running tile and static data servers..."
	@{ \
		uvicorn app:app --host 0.0.0.0 --port ${TILER_PORT} --workers ${WORKERS} & \
		uvicorn serve_data:app --host 0.0.0.0 --port ${DATA_PORT} --workers 1 & \
		wait ;\
	}

run-dev: build
	# Passing `--env` for Procfile that `honcho` relies on

	docker run -it --rm \
		-p ${TILER_PORT}:${TILER_PORT} \
		-p ${DATA_PORT}:${DATA_PORT} \
		-v ${shell pwd}/data/:/app/mounted_vols/data/ \
		--env TILER_PORT=${TILER_PORT} \
		--env DATA_PORT=${DATA_PORT} \
		--env WORKERS=${WORKERS} \
		--env DATA_DIR=${DOCKER_DATA_DIR} \
		$(IMAGE_NAME)

remove-image:
	docker rmi ${IMAGE_NAME}
