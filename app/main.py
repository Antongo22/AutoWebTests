from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return templates.TemplateResponse(
        "calculator.html",
        {"request": request, "error": "Некорректный ввод данных"},
        status_code=400
    )

@app.get("/", response_class=HTMLResponse)
async def calculator_page(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})

@app.get("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    num1: str,
    num2: str,
    operation: str
):
    try:
        num1 = num1.strip()
        num2 = num2.strip()
        
        if not num1 or not num2:
            raise HTTPException(status_code=400, detail="Пустые значения")
            
        num1_float = float(num1)
        num2_float = float(num2)

        result = None  
        if operation == "add":
            result = num1_float + num2_float
        elif operation == "subtract":
            result = num1_float - num2_float
        elif operation == "multiply":
            result = num1_float * num2_float
        elif operation == "divide":
            if num2_float == 0:
                raise HTTPException(status_code=400, detail="Деление на ноль")
            result = num1_float / num2_float
        else:
            raise HTTPException(status_code=400, detail="Неверная операция")

        return templates.TemplateResponse(
            "calculator.html",
            {
                "request": request,
                "result": round(result, 2),
                "error": None
            }
        )

    except ValueError:
        return templates.TemplateResponse(
            "calculator.html",
            {
                "request": request,
                "result": None,
                "error": "Некорректный формат числа"
            },
            status_code=400
        )
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "calculator.html",
            {
                "request": request,
                "result": None,
                "error": e.detail
            },
            status_code=e.status_code
        )