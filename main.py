from fastapi import FastAPI
from controllers.get_controller import get_router
from controllers.post_controller import post_router
from controllers.patch_controller import patch_router
from controllers.delete_controller import delete_router


app = FastAPI()
app.include_router(get_router)
app.include_router(post_router)
app.include_router(patch_router)
app.include_router(delete_router)
