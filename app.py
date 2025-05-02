from fastapi import FastAPI
from fastapi.responses import RedirectResponse
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

@app.get("/")
def root():
    return {
        "message": "Use /tiles/{hemisphere}/{forecast_date}/{leadtime}/tilejson.json to fetch TileJSON"
    }

from rio_tiler.colormap import ColorMaps

@app.get("/utils/colormaps")
async def colormaps():
    return ColorMaps().list()
