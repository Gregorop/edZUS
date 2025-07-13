from fastapi import FastAPI
from app.core.one_action_formula.crud import router as formulas_router

app = FastAPI()
app.include_router(formulas_router)


@app.get("/")
async def hello():
    return {"edZUS": "education Zoomers Upgrade System"}
