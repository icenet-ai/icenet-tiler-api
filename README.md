> [!WARNING]
> DEPRECATED
>
> This is the code base for serving image tiles for use with corresponding Plotly dashboard.
>
> It has been replaced by a docker container in the orchestrating repo.

# environmental-tiler-api

This repository contains API backend supporting [`environmental-stac-dashboard`]((https://github.com/environmental-forecasting/environmental-stac-dashboard)). It is built on top of [Titiler](https://github.com/developmentseed/titiler) and [FastAPI](https://fastapi.tiangolo.com/) to serve Cloud Optimized GeoTIFF (COG) files from [icenet](https://github.com/icenet-ai/icenet).

## Usage

This application is designed to be used in conjunction with [environmental-stac-dashboard](https://github.com/environmental-forecasting/environmental-stac-dashboard). It serves COG files and STAC catalogs from a configurable directory, which can be mounted as a volume or passed via an environment variable.

This codebase contains two apps which are to be run concurrently, `app.py` and `serve_data.py`.

- [`app.py`](app.py):

    TiTiler-based FastAPI application, including route definitions for COG and STAC tilers.

- [`serve_data.py`](serve_data.py):

    FastAPI server to serve static data from a configurable directory (by default, `./data`). This is used to serve the static files, such as STAC catalogs and COG files.

## Installation and Setup

If you are attempting to run this independent of the orchestrating repository (`environmental-stac-orchestrator`), then, make sure to first convert the IceNet netCDF predictions to COG using `environmental-stac-generator` first which will create a `data/` directory at the root of this repository (assuming you're running the conversion command from this path). Then, you can run this independent of the orchestrator repo.

### 1. Clone the repository

```bash
git clone https://github.com/environmental/environmental-tiler-api.git
cd environmental-tiler-api
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

