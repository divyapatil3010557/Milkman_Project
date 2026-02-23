from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from .routers import users, products, customers, subscriptions

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Milkman API", description="API for milkman subscription management")

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include Routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(subscriptions.router)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")
