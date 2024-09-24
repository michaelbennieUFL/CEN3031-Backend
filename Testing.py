from flask import Blueprint,jsonify

test_bp=Blueprint("lp", __name__, url_prefix="/testing")


@test_bp.route('/TestRoute')
def get_languages():
    return jsonify({"Hello": "World"})