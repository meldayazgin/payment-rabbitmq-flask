from flask import request, jsonify
import json
from rabbitmq import channel, delay_execution
import pika

def setup_routes(app):
    @app.route('/make-payment', methods=['POST'])
    def process_payment_request():
        delay_execution()
        try:
            data = request.json
            user = data.get('user')
            payment_type = data.get('paymentType')
            card_no = data.get('cardNo')

            if not user or not payment_type or not card_no:
                return jsonify({"error": "Missing input."}), 400

            message = json.dumps(data)

            try:
                channel.basic_publish(
                    exchange='',
                    routing_key='payment_queue',
                    body=message,
                    properties=pika.BasicProperties(delivery_mode=2)
                )
                print("Payment request sent to the queue.")
            except Exception as e:
                print(f"Error sending payment message: {e}")
                return jsonify({"error": f"Could not send payment request: {str(e)}"}), 500

            return jsonify({"message": "Payment request sent successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
