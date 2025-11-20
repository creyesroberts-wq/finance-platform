from fastapi import APIRouter

router = APIRouter()

@router.get("/corporate")
def get_corporate():
    return {"message": "Corporate Finance API working!"}
