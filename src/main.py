from fastapi import FastAPI

from src.routers import product_router, category_router
app = FastAPI()
app.include_router(product_router.router)
app.include_router(category_router.router)


@app.get('')
async def main_page():
    return {'text': 'ok'}
