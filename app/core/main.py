from fastapi import FastAPI
from app.core.one_action_formula.crud import router as formulas_router
from app.core.theory.crud import router as theory_router
from app.core.tasks.crud import router as tasks_router

app = FastAPI()
app.include_router(formulas_router)
app.include_router(theory_router)
app.include_router(tasks_router)


@app.get("/")
async def hello():
    return {"edZUS": "education Zoomers Upgrade System"}
