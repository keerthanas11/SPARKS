from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__, static_url_path='/static')

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="keeru2004",
        database="new"
    )

# Function to get customers
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email, name, current_balance FROM bank")
    customers = cursor.fetchall()
    conn.close()
    return customers

@app.route('/')
def index():
    customers = get_customers()
    return render_template('index1.html', customers=customers)

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    from_email = data['fromEmail']
    to_email = data['toEmail']
    amount = float(data['amount'])

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if from_email exists
    cursor.execute("SELECT current_balance FROM bank WHERE email = %s", (from_email,))
    from_balance = cursor.fetchone()
    if from_balance is None:
        app.logger.error(f"Sender email not found: {from_email}")
        return jsonify({'message': 'Invalid email address for sender.'}), 400

    # Check if to_email exists
    cursor.execute("SELECT current_balance FROM bank WHERE email = %s", (to_email,))
    to_balance = cursor.fetchone()
    if to_balance is None:
        app.logger.error(f"Recipient email not found: {to_email}")
        return jsonify({'message': 'Invalid email address for recipient.'}), 400

    # Check for sufficient balance
    if from_balance[0] < amount:
        app.logger.error(f"Insufficient balance for email: {from_email}")
        return jsonify({'message': 'Insufficient balance.'}), 400

    # Perform the transfer
    new_from_balance = from_balance[0] - amount
    new_to_balance = to_balance[0] + amount

    cursor.execute("UPDATE bank SET current_balance = %s WHERE email = %s", (new_from_balance, from_email))
    cursor.execute("UPDATE bank SET current_balance = %s WHERE email = %s", (new_to_balance, to_email))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': f'{amount} has been transferred from {from_email} to {to_email}.'})

if __name__ == '__main__':
    app.run(debug=True)
