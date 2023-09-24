from database import SessionLocal

class DatabaseManager:

    @staticmethod
    def shutdown_event():
        # Close Any Open Connections
        db = SessionLocal()
        db.close()

    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
