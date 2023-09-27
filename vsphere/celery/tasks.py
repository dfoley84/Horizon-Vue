from celery import Celery
from jenkins import jenkinsbuild  

# Configure Celery app
app = Celery('tasks', broker='pyamqp://guest:guest@localhost/vsphere')

@app.task
def print_message(body):
    print(f"Received message: {body}")

    # Extract the contents of the message
    try:
        content = body.get('currentUser', {})
        for key, value in content.items():
            print(f"{key}: {value}")
              #Call the Jenkinsbuild python Script 
        
      


    except Exception as e:
        print(f"Error parsing message: {e}")

