import logging
import paramiko
import asyncio
from fastapi import FastAPI, WebSocket, APIRouter, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import models


from dbconnect import DatabaseManager

router = APIRouter()




@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    print("WebSocket route accessed") 
    await websocket.accept()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print("Before SSH connect")
        ssh_client.connect('172.31.165.88', port=22, username='dfoley', password='sony84')
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
        ssh_client.close()
