from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import models


from dbconnect import DatabaseManager

router = APIRouter()

def shutdown_event():
    DatabaseManager.shutdown_event()


@router.get("/")

async def search(db: Session = Depends(DatabaseManager.get_db)):
    response_object = {'status': 'success'}
    response_object['vdesksearch'] = db.query(models.Horizon).all()
    print(jsonable_encoder(response_object))
    return JSONResponse(jsonable_encoder(response_object))





