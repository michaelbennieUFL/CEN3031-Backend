from flask import Blueprint, jsonify, request

from DataModels import *
from Extensions import DATABASE as db
user_bp=Blueprint("user", __name__, url_prefix="/user")



# Route for setting (creating/updating) a user
@user_bp.route('/', methods=['POST'])
def set_user():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({'error': 'Missing user id'}), 400

    user_id = data['id']
    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id)

    # Update user fields
    user.picture = data.get('picture')
    user.family_name = data.get('family_name', '')
    user.given_name = data.get('given_name', '')
    user.email = data.get('email', '')
    user.preferred_firstname = data.get('preferred_firstname')
    user.preferred_lastname = data.get('preferred_lastname')
    user.preferred_email = data.get('preferred_email')
    user.school_year = data.get('school_year')

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User saved successfully'}), 200

# Route for retrieving user information based on user id
@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200