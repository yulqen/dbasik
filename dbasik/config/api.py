from dbasik.datamap.api import router as datamap_router
from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/datamap/", datamap_router)
