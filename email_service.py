from flask_mail import Message
from flask import current_app
import json
from time import sleep

def send_confirmation_email(ch, method, properties, body):
    delay_execution()
    try:
        notification_data = json.loads(body)
        user = notification_data.get('user')
        payment_type = notification_data.get('paymentType')

        if not user or not payment_type:
            print("Missing input.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        with current_app.app_context():
            mail = current_app.extensions['mail']
            msg = Message(
                subject="Payment Successful",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user]
            )
            msg.body = (
                f"Hi,\n\n"
                f"Your payment was successful! "
                f"Thank you for using our service!\n\n- Melda"
            )
            mail.send(msg)
            print(f"Email sent to {user}.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error sending email: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def delay_execution(seconds=2):
    sleep(seconds)
