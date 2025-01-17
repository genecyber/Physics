from flask import Blueprint, current_app, request, jsonify

bp = Blueprint('cosmological', __name__)

@bp.route('/update_density', methods=['POST'])
def update_density():
    data = request.json
    density = data.get('density')
    current_app.event_bus.publish('density_updated', density)
    return jsonify({"message": "Density updated successfully"}), 200

def handle_density_update(data):
    print(f"Updated density received: {data}")

def init_app(app):
    app.event_bus.subscribe('density_updated', handle_density_update)
