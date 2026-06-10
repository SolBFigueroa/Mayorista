from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import usuarios, productos, ventas
from app.routes import productos, usuarios, ventas
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"], # backend acepta peticiones de esas urls
    allow_methods=["*"], # * = todos
    allow_headers=["*"],
)
# acá van a ir los routers después
app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(ventas.router)



