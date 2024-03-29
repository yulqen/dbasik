from dbasik.datamap.api import router as datamap_router
from dbasik.register.api import router as register_router
from dbasik.returns.api import router as returns_router
from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/datamap/", datamap_router)
api.add_router("/register/", register_router)
api.add_router("/returns/", returns_router)
