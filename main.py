from fastapi import FastAPI
from app.database import engine, Base
from app.models import usuarios, productos, ventas
from app.routes import productos
Base.metadata.create_all(bind=engine)

app = FastAPI()
# acá van a ir los routers después
app.include_router(productos.router)




