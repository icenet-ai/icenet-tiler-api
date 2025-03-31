from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from pystac import Catalog
from rio_tiler.io import Reader, STACReader

from titiler.core.factory import (
    MultiBaseTilerFactory,
    TilerFactory,
)
from titiler.extensions import (
    cogValidateExtension,
    cogViewerExtension,
    stacExtension,
    stacViewerExtension,
)

app = FastAPI()

# Load STAC Catalog
STAC_PATH = Path("data/stac/catalog.json")
COG_DIR = Path("data/cogs")

# Load the STAC catalog from the local file
catalog = Catalog.from_file(STAC_PATH)

# Create a tiler for COGs
cog_tiler = TilerFactory(
    reader=Reader,
    router_prefix="/cog",
    extensions=[
        cogValidateExtension(),
        cogViewerExtension(),
        stacExtension(),
    ],
)

# Add the tiler to the main FastAPI app
app.include_router(cog_tiler.router, prefix="/cog", tags=["Cloud Optimized GeoTIFF"])

stac_tiler = MultiBaseTilerFactory(
    reader=STACReader,
    router_prefix="/stac",
    extensions=[
        stacViewerExtension(),
    ],
)

app.include_router(
    stac_tiler.router, prefix="/stac", tags=["SpatioTemporal Asset Catalog"]
)


@app.get("/tiles/{hemisphere}/{forecast_date}/{leadtime}/tilejson.json")
async def get_tilejson(
    hemisphere: str,
    forecast_date: str,
    leadtime: int,
    tile_format: str = Query("png", enum=["png", "jpeg", "webp"]),
):
    """
    Generate and serve TileJSON for a specific COG.
    """
    # Search STAC catalog for the matching GeoTIFF
    # In my definition, a catalog contains a collection of forecast_start_dates, with north and south within it.
    collection = next(
        (c for c in catalog.get_children() if c.id == f"forecast-{forecast_date}"), None
    )
    print("Collections:", list(catalog.get_children()))
    # exit()
    if not collection:
        raise HTTPException(status_code=404, detail="Forecast date not found")

    # Match the item based on hemisphere and leadtime
    item = next(
        (
            i
            for i in collection.get_items()
            if i.properties["hemisphere"] == hemisphere
            and i.properties["leadtime"] == leadtime
        ),
        None,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Matching GeoTIFF not found")

    geotiff_href = item.assets["geotiff"].href
    geotiff_file_path = Path(geotiff_href)

    if not geotiff_file_path.exists():
        raise HTTPException(
            status_code=404, detail=f"GeoTIFF file not found: {geotiff_file_path}"
        )

    # Construct the TileJSON URL using the local file path
    tilejson_url = f"/cog/WebMercatorQuad/tilejson.json?url={geotiff_file_path}&colormap_name=viridis&rescale=0,1"

    # Redirect to the dynamically created TileJSON endpoint
    return RedirectResponse(tilejson_url)


@app.get("/")
def root():
    return {
        "message": "Use /tiles/{hemisphere}/{forecast_date}/{leadtime}/tilejson.json to fetch TileJSON"
    }

from rio_tiler.colormap import ColorMaps

@app.get("/utils/colormaps")
async def colormaps():
    return ColorMaps().list()
