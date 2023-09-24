from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import models


from dbconnect import DatabaseManager

router = APIRouter()

def shutdown_event():
    DatabaseManager.shutdown_event()


@router.post("/")

async def HorizonServers(request: Request, db: Session = Depends(DatabaseManager.get_db)):
    response_object = {'status': 'success'}
    data = await request.json()
    currentUser  = data['currentUser']
    response_object['SearchvDesks'] = db.query(models.Horizon).filter(models.Horizon.UserName == currentUser).all()
    return JSONResponse(jsonable_encoder(response_object))





