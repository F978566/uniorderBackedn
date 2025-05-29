from fastapi import FastAPI, Request
from dishka.integrations.fastapi import setup_dishka
import uvicorn
from dotenv import load_dotenv

from di.providers import container
from presentation.api.auth import auth_router
from presentation.api.restaurant import restaurant_router
from presentation.api.files import files_router
from presentation.api.branch_office import branch_office_router
from presentation.api.menu import menu_router
from presentation.api.order import order_router

load_dotenv()
app = FastAPI()
setup_dishka(container, app)
app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(files_router)
app.include_router(branch_office_router)
app.include_router(menu_router)
app.include_router(order_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request URL: {request.url}")
    print(f"Authorization: {request.headers.get('authorization')}")
    print(f"Request Headers: {request.headers}")
    # if request.headers.get("content-type", "").startswith("multipart/form-data"):
    #     form_data = await request.form()
    #     print("Form Data:")
    #     for key, value in form_data.items():
    #         if isinstance(value, UploadFile):
    #             print(f"{key}: filename={value.filename}, size={value.size}")
    #         else:
    #             print(f"{key}: {value}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="10.162.192.114", port=8000)
