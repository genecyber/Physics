from flask import Blueprint, current_app, request, jsonify

bp = Blueprint('statistical_mechanics', __name__)

@bp.route('/update_density_matrix', methods=['POST'])
def update_density_matrix():
    data = request.json
    density_matrix = data.get('density_matrix')
    current_app.event_bus.publish('density_matrix_updated', density_matrix)
    return jsonify({"message": "Density matrix updated successfully"}), 200

def handle_density_matrix_update(data):
    print(f"Updated density matrix received: {data}")

def init_app(app):
    app.event_bus.subscribe('density_matrix_updated', handle_density_matrix_update)
