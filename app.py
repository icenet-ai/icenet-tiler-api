from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from rio_tiler.colormap import ColorMaps
from rio_tiler.io import Reader, STACReader

from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
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
from titiler.mosaic.errors import MOSAIC_STATUS_CODES

app = FastAPI()

# Add exception handlers - Won't show lots of missingtiles warnings when outside of bounds.
add_exception_handlers(app, DEFAULT_STATUS_CODES)
add_exception_handlers(app, MOSAIC_STATUS_CODES)

# Create a tiler for COGs
cog_tiler = TilerFactory(
    reader=Reader,
    router_prefix="/cog",
    extensions=[
        cogValidateExtension(),
        cogViewerExtension(),
    ],
)

# Not currently used for IceNet dashboard, but, would be nice to dig into this at some point.
stac_tiler = MultiBaseTilerFactory(
    reader=STACReader,
    router_prefix="/stac",
    extensions=[
        stacExtension(),
        stacViewerExtension(),
    ],
)

# Add titiler routers to the main FastAPI app
app.include_router(cog_tiler.router, prefix="/cog", tags=["Cloud Optimised GeoTIFF"])

app.include_router(
    stac_tiler.router, prefix="/stac", tags=["SpatioTemporal Asset Catalog"]
)


# Don't find the non-existent main root to be useful, point to Swagger docs instead
@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"


@app.get("/utils/colormaps")
async def colormaps():
    return ColorMaps().list()
