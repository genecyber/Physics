from flask import Blueprint, current_app, request, jsonify

bp = Blueprint('electromagnetic', __name__)

@bp.route('/update_field_tensor', methods=['POST'])
def update_field_tensor():
    data = request.json
    field_tensor = data.get('field_tensor')
    current_app.event_bus.publish('field_tensor_updated', field_tensor)
    return jsonify({"message": "Field tensor updated successfully"}), 200

def handle_field_tensor_update(data):
    print(f"Updated field tensor received: {data}")

def init_app(app):
    app.event_bus.subscribe('field_tensor_updated', handle_field_tensor_update)
