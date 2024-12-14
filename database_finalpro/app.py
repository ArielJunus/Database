from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId

# Initialize Flask app and MongoDB client
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.flask_database
expenses_collection = db.expenses

# HTML template as a string
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.form
    expense = {
        "category": data['category'],
        "amount": float(data['amount']),
        "date": data['date']
    }
    result = expenses_collection.insert_one(expense)
    return jsonify({'status': 'success', 'id': str(result.inserted_id)}), 200

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    expenses = list(expenses_collection.find())
    for expense in expenses:
        expense['id'] = str(expense.pop('_id'))
    total_amount = sum(exp['amount'] for exp in expenses)
    return jsonify({'expenses': expenses, 'total_amount': total_amount})

@app.route('/edit_expense/<string:expense_id>', methods=['PUT'])
def edit_expense(expense_id):
    data = request.get_json()  # Fetch JSON payload
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    category = data.get('category')
    amount = data.get('amount')
    date = data.get('date')

    # Check for missing fields
    if not category or not amount or not date:
        return jsonify({"error": "Missing fields"}), 400

    try:
        # Add extra validation if needed (e.g., check amount is a positive number)
        amount = float(amount)  # Ensure amount is a valid number
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
        # Add more validation for the date field if needed (e.g., check format)

        # Convert expense_id to ObjectId
        expense_id = ObjectId(expense_id)

        # Update logic for your database
        updated = update_expense_in_db(expense_id, category, amount, date)
        if updated:
            return jsonify({"message": "Expense updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update expense"}), 500
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def update_expense_in_db(expense_id, category, amount, date):
    # Replace with actual database logic
    try:
        result = expenses_collection.update_one(
            {'_id': expense_id},  # Find the document by its ObjectId
            {'$set': {'category': category, 'amount': amount, 'date': date}}  # Update fields
        )
        # If at least one document was modified
        if result.modified_count > 0:
            return True
        else:
            return False  # If no document was modified (could be because the data is the same)
    except Exception as e:
        print(f"Error updating expense: {e}")
        return False


@app.route('/delete_expense/<string:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    result = expenses_collection.delete_one({'_id': ObjectId(expense_id)})
    if result.deleted_count:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Expense not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

