from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import models
from dbconnect import DatabaseManager

class UpdateMachine:
    
    @staticmethod
    def update_machine_status(MachineName: str, vDeskAction:str, db: Session):
        machine = db.query(models.Horizon).filter(models.Horizon.MachineName == MachineName).first()
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        
        if vDeskAction != 'Delete':
            machine.MachineStatus = "Running Job"
            db.commit()
            return {"message": "Machine status updated successfully"}

        elif vDeskAction == 'Delete':
            print('Deleteing Machine')
            db.delete(machine)
            db.commit()
            return {"message": "Machine deleted successfully"}
        

    