from flask import Blueprint, current_app, request, jsonify

bp = Blueprint('general_relativity', __name__)

@bp.route('/update_metric_tensor', methods=['POST'])
def update_metric_tensor():
    data = request.json
    metric_tensor = data.get('metric_tensor')
    current_app.event_bus.publish('metric_tensor_updated', metric_tensor)
    return jsonify({"message": "Metric tensor updated successfully"}), 200

def handle_metric_tensor_update(data):
    print(f"Handling metric tensor update: {data}")

def init_app(app):
    app.event_bus.subscribe('metric_tensor_updated', handle_metric_tensor_update)
