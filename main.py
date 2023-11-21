from fastapi import FastAPI
import uvicorn
from src.routes import user_profile
from src.routes import auth
from src.routes import photo
from src.routes import roles
from src.routes import tags
# from src.routes import comments

app = FastAPI()
app.include_router(auth.router, prefix="/api")
app.include_router(user_profile.profile_router, prefix="/api")
app.include_router(roles.router, prefix='/api')
app.include_router(photo.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
# app.include_router(comments.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "REST APP v1.0"}

if __name__ == "__main__":
    uvicorn.run(app)