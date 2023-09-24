import pika, json

class RabbitMQSender:

    EXCHANGE_NAME = 'vSphere_direct_exchange'
    QUEUE_NAME = 'vSphere_queue'
    ROUTING_KEY = 'vSphere_routing_key'

    @staticmethod
    def send(message: dict):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            # Declare a direct exchange
            channel.exchange_declare(exchange=RabbitMQSender.EXCHANGE_NAME, exchange_type='direct')
            
            # Declare the queue
            channel.queue_declare(queue=RabbitMQSender.QUEUE_NAME, durable=False)
            
            # Bind the queue to the direct exchange with a routing key
            channel.queue_bind(exchange=RabbitMQSender.EXCHANGE_NAME, 
                               queue=RabbitMQSender.QUEUE_NAME, 
                               routing_key=RabbitMQSender.ROUTING_KEY)

            # Publish the message with the routing key
            channel.basic_publish(
                exchange=RabbitMQSender.EXCHANGE_NAME,
                routing_key=RabbitMQSender.ROUTING_KEY,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except Exception as e:
            print(f"Failed to send message to RabbitMQ: {e}")
        finally:
            if connection:
                connection.close()
