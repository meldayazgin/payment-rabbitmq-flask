from flask import Flask
from flask_mail import Mail
from threading import Thread
from config import MAIL_CONFIG
from rabbitmq import initialize_rabbitmq_consumers
from routes import setup_routes

app = Flask("messageapp")
app.config.update(MAIL_CONFIG)

mail = Mail(app)
setup_routes(app)

if __name__ == "__main__":

    consumer_thread = Thread(target=initialize_rabbitmq_consumers, args=(app,))
    consumer_thread.daemon = True
    consumer_thread.start()

    app.run(debug=True, host='0.0.0.0', port=5000)
