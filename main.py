import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import get_films
from fastapi.templating import Jinja2Templates
from parse import main

app = FastAPI()
# Монтируем статические файлы для директорий "table" и "img"
app.mount("/static", StaticFiles(directory="table"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="img")

templates = Jinja2Templates(directory='table')
#Кореневой путь
@app.get("/", response_class=FileResponse)
def root_html():
    return "table/index.html"
#Путь до таблицы
@app.get("/search")
def table_html(request: Request):
    main()
    table = get_films()
    return templates.TemplateResponse("table.html", {"request": request, "data": sorted(table, key=lambda x: x.raiting, reverse=True)})

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8080)