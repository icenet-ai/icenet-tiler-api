export TAG        ?= "dev"
export TILER_PORT ?= 8000
export DATA_PORT  ?= 8002
export WORKERS    ?= 12
IMAGE_NAME = "icenet-dashboard/plotly-dash-web-dashboard:$(TAG)"

build:
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Starting tile and static data servers with honcho (PORTS: $(TILER_PORT), $(DATA_PORT), WORKERS: $(WORKERS))"
	@honcho start

dev:
	@echo "Running tile and static data servers..."
	@{ \
		uvicorn app:app --port ${TILER_PORT} --workers ${WORKERS} & \
		uvicorn serve_data:app --port ${DATA_PORT} --workers 1 & \
		wait ;\
	}

run-dev: build
	docker run -it --rm -p 8000:8000 -v ${shell pwd}/data/:/app/mounted_vols/data/ $(IMAGE_NAME)

remove-image:
	docker rmi ${IMAGE_NAME}
