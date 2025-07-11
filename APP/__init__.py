from fastapi import FastAPI
from APP.db import engine, SessionLocal
from APP.models import dispositivo
from APP import models
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from APP.views.auth import router as auth_router 
from APP.views.glpi import router as glpi_router
from APP.views.formulario_entrega import router as formulario_entrega_router
from APP.views.formulario_devolucion import router as formulario_devolucion_router
from APP.views.stock_1 import router as stock_1_router
from APP.views.stock_2 import router as stock_2_router
from APP.views.leasing import router as leasing_router
from APP.views.home import router as home_router
from dotenv import load_dotenv
import os


load_dotenv()
secret_key = os.getenv("SECRET_KEY")

app = FastAPI()
app.include_router(auth_router)
app.include_router(glpi_router)
app.include_router(formulario_entrega_router)
app.include_router(formulario_devolucion_router)
app.include_router(stock_1_router)
app.include_router(stock_2_router)
app.include_router(home_router)
app.include_router(leasing_router)
app.mount("/static", StaticFiles(directory="APP/static"), name="static") 
app.add_middleware(SessionMiddleware, secret_key=secret_key) 
models.Base.metadata.create_all(bind=engine)
