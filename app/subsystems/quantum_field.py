from flask import Blueprint, current_app, request, jsonify

bp = Blueprint('quantum_field', __name__)

@bp.route('/update_scalar_field', methods=['POST'])
def update_scalar_field():
    data = request.json
    scalar_field = data.get('scalar_field')
    current_app.event_bus.publish('scalar_field_updated', scalar_field)
    return jsonify({"message": "Scalar field updated successfully"}), 200

def handle_scalar_field_update(data):
    print(f"Updated scalar field received: {data}")

def init_app(app):
    app.event_bus.subscribe('scalar_field_updated', handle_scalar_field_update)
