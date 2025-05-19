# icenet-tiler-api

This repository contains API backend supporting [`icenet-dashboard`]((https://github.com/icenet-ai/icenet-dashboard)). It is built on top of [Titiler](https://github.com/developmentseed/titiler) and [FastAPI](https://fastapi.tiangolo.com/) to serve Cloud Optimized GeoTIFF (COG) files from [icenet](https://github.com/icenet-ai/icenet).

## Usage

This application is designed to be used in conjunction with [icenet-dashboard](https://github.com/icenet-ai/icenet-dashboard). It serves COG files and STAC catalogs from a configurable directory, which can be mounted as a volume or passed via an environment variable.

This codebase contains two apps which are to be run concurrently, `app.py` and `serve_data.py`.

- [`app.py`](app.py):

    TiTiler-based FastAPI application, including route definitions for COG and STAC tilers.

- [`serve_data.py`](serve_data.py):

    FastAPI server to serve static data from a configurable directory (by default, `./data`). This is used to serve the static files, such as STAC catalogs and COG files.

## Installation and Setup

If you are attempting to run this independent of the orchestrating repository (`icenet-dashboard-meta`), then, make sure to first convert the IceNet netCDF predictions to COG using `icenet-dashboard-preprocessor` first which will create a `data/` directory at the root of this repository (assuming you're running the conversion command from this path). Then, you can run this independent of the orchestrator repo.

### 1. Clone the repository

```bash
git clone https://github.com/icenet-ai/icenet-tiler-api.git
cd icenet-tiler-api
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Run the applications

```bash
make run
```

This will run both `app.py` and `serve_data.py` across ports `8000` and `8002` respectively. The API docs can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs).
