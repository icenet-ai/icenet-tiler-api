TAG ?= "dev"
WORKERS ?= 12
IMAGE_NAME = "icenet-dashboard/plotly-dash-web-dashboard:$(TAG)"

build:
	docker build -t $(IMAGE_NAME) .
run:
	uvicorn app:app --host 0.0.0.0 --port 8000 --workers ${WORKERS}

run-dev: build
	docker run -it --rm -p 8000:8000 --workers ${WORKERS} -v ${pwd}/data/:/app/mounted_vols/data/ $(IMAGE_NAME)

remove-image:
	docker rmi ${IMAGE_NAME}
