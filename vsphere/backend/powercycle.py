from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import json


from dbconnect import DatabaseManager
from updateMachine import UpdateMachine
from rabbitmq import RabbitMQSender

def shutdown_event():
    DatabaseManager.shutdown_event()
router = APIRouter()

# Other imports ...

@router.post("/")
async def selectedMachine(item: dict, db: Session = Depends(DatabaseManager.get_db)):
    message = json.loads(json.dumps(item, indent=2))
    MachineName = message['currentUser']['vDesk']['MachineName']
    vDeskAction = message['currentUser']['PowerCycle']

    if MachineName and vDeskAction:
        if vDeskAction != 'Delete':
            RabbitMQSender.send(message=item)
           
        result = UpdateMachine.update_machine_status(MachineName, vDeskAction, db)

    else:
        result = {"message": "Machine name or action not provided in the request"}

    return JSONResponse(content=jsonable_encoder({'status': 'success', 'result': result}))
