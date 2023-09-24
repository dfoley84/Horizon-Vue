import logging
import paramiko
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
=======
from sqlalchemy.orm import Session
from database import SessionLocal
from rabbitmq import RabbitMQ_Sender
import models
import json
>>>>>>> a60a5bbb8959cfd0a64439707f8870d35754a069

from horizon import router as HorizonRouter
from powercycle import router as PowerCycleRouter
from search import router as SearchRouter

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(HorizonRouter, prefix='/vdesk', tags=['Horizon'])
app.include_router(PowerCycleRouter, prefix='/powercycle', tags=['PowerCycle'])
app.include_router(SearchRouter, prefix='/search', tags=['Search'])



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("WebSocket route accessed") 
    await websocket.accept()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print("Before SSH connect")
        ssh_client.connect('', port=22, username='', password='')  #Needs to be updated to pass IP Address, Username from DB Query
        print("Connected to SSH")
    except Exception as e:
        logging.error(f"Error connecting to SSH: {e}")
        await websocket.send_text(f"Error connecting to SSH: {e}")
        await websocket.close()
        return

    async def receive_from_ssh():
        while True:
            if chan.recv_ready():
                ssh_response = chan.recv(256).decode('utf-8')
                await websocket.send_text(ssh_response)
            await asyncio.sleep(0.1)

    chan = ssh_client.invoke_shell()
    asyncio.create_task(receive_from_ssh())

    try:
        while True:
            data = await websocket.receive_text()  
            chan.send(data)
    except WebSocketDisconnect:
        logging.warning("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Error during WebSocket communication: {e}")
        await websocket.send_text(f"Error: {e}")
    finally:
<<<<<<< HEAD
        ssh_client.close()
=======
        db.close()

#Search for a specific User
@app.get("/horizon")
async def HorizonServers(
    db: Session = Depends(get_db)
): 
    response_object = {'status': 'success'}
    response_object['vdesks']  = db.query(models.Horizon).all()
    return JSONResponse(content=jsonable_encoder(response_object))

#Search for a specific User
@app.post("/searchdata")
async def HorizonServers(
    request: Request,
    db: Session = Depends(get_db)
): 
    response_object = {'status': 'success'}
    data = await request.json()
    user = data['TitleUser']
    print(user)
    response_object['SearchvDesks']  = db.query(models.Horizon).filter(models.Horizon.UserName == user).all()
    return JSONResponse(content=jsonable_encoder(response_object))


@app.post("/powercycle")
async def selectedMachine(item: dict):
    message = json.loads(json.dumps(item, indent=2))
  
  
    print(message['data']['PowerCycle'])
    print(message['data']['vDesk']['MachineName'])
    
    RabbitMQ_Sender(message) #Passing Message to Class RabbitMQ_Sender
    return JSONResponse(content=jsonable_encoder({'status': 'success'}))
>>>>>>> a60a5bbb8959cfd0a64439707f8870d35754a069
