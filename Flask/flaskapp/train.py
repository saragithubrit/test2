from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for tickets and user details
tickets = []
users = {}


@app.route('/purchase_ticket', methods=['POST'])
def purchase_ticket():
    data = request.get_json()

    from_location = data.get('from_location')
    to_location = data.get('to_location')
    user = data.get('user')
    price_paid = 20  # Fixed price for the ticket

    # Assume there are only two sections A and B
    section = 'A' if len(tickets) % 2 == 0 else 'B'

    # Allocate a seat
    seat = len(tickets) + 1

    ticket = {
        'from': from_location,
        'to': to_location,
        'user': user,
        'price_paid': price_paid,
        'section': section,
        'seat': seat
    }

    tickets.append(ticket)
    users[user['email']] = {'section': section, 'seat': seat}

    return jsonify({'message': 'Ticket purchased successfully', 'ticket': ticket})


@app.route('/get_receipt/<user_email>', methods=['GET'])
def get_receipt(user_email):
    if user_email in users:
        user_details = users[user_email]
        ticket = [t for t in tickets if t['user']['email'] == user_email][0]
        return jsonify({'user_details': user_details, 'ticket': ticket})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/get_users_by_section/<section>', methods=['GET'])
def get_users_by_section(section):
    section_users = [{'user': ticket['user'], 'seat': ticket['seat']} for ticket in tickets if ticket['section'] == section]
    return jsonify({'section': section, 'users': section_users})


@app.route('/remove_user/<user_email>', methods=['DELETE'])
def remove_user(user_email):
    if user_email in users:
        user_details = users[user_email]
        tickets[:] = [ticket for ticket in tickets if ticket['user']['email'] != user_email]
        del users[user_email]
        return jsonify({'message': 'User removed successfully', 'user_details': user_details})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/modify_seat/<user_email>', methods=['PUT'])
def modify_seat(user_email):
    if user_email in users:
        data = request.get_json()
        new_seat = data.get('new_seat')

        if new_seat is not None:
            ticket = [t for t in tickets if t['user']['email'] == user_email][0]
            ticket['seat'] = new_seat
            users[user_email]['seat'] = new_seat

            return jsonify({'message': 'Seat modified successfully', 'new_seat': new_seat})
        else:
            return jsonify({'message': 'Invalid request. Please provide new_seat parameter'}), 400
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8080)
