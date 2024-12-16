from flask import current_app
import pika
import json
from time import sleep
from email_service import send_confirmation_email


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='payment_queue', durable=True)
channel.queue_declare(queue='notification_queue', durable=True)

def delay_execution(seconds=3):
    sleep(seconds)

def handle_payment_processing(ch, method, properties, body):
    delay_execution()
    try:
        payment_data = json.loads(body)
        print(f"Processing payment: {payment_data}")

        notification_data = {
            'user': payment_data['user'],
            'paymentType': payment_data['paymentType']
        }

        channel.basic_publish(
            exchange='',
            routing_key='notification_queue',
            body=json.dumps(notification_data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"Notification sent: {notification_data}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing payment: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def initialize_rabbitmq_consumers(app):
    delay_execution()

    with app.app_context():
        try:
            channel.basic_consume(queue='payment_queue', on_message_callback=handle_payment_processing)
            channel.basic_consume(queue='notification_queue', on_message_callback=send_confirmation_email)
            print("Waiting for messages...")
            channel.start_consuming()
        except Exception as e:
            print(f"RabbitMQ consumer error: {e}")
