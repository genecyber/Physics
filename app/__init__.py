from flask import Flask, send_from_directory, jsonify, Response, request, send_file
import os
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='/app/static', static_url_path='')
    CORS(app)  # Enable CORS for all routes

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if not path:
            return send_from_directory('/app/static', 'index.html')
        try:
            return send_from_directory('/app/static', path)
        except:
            return send_from_directory('/app/static', 'index.html')

    # Debug endpoint to check static files
    @app.route('/debug/static')
    def debug_static():
        static_files = []
        for root, dirs, files in os.walk('/app/static'):
            for file in files:
                static_files.append(os.path.join(root, file))
        return jsonify({
            'static_files': static_files,
            'static_folder': app.static_folder,
            'static_url_path': app.static_url_path
        })

    # API Endpoints
    @app.route('/general_relativity/update_metric_tensor', methods=['POST'])
    def update_metric_tensor():
        data = request.get_json()
        metric_tensor = data.get('metric_tensor')
        print(f"Updating metric tensor: {metric_tensor}")
        # Add your physics calculations here
        return jsonify({
            "status": "success",
            "message": "Metric tensor updated",
            "value": metric_tensor
        })

    @app.route('/quantum_field/update_scalar_field', methods=['POST'])
    def update_scalar_field():
        data = request.get_json()
        scalar_field = data.get('scalar_field')
        print(f"Updating scalar field: {scalar_field}")
        # Add your physics calculations here
        return jsonify({
            "status": "success",
            "message": "Scalar field updated",
            "value": scalar_field
        })

    @app.route('/cosmological/update_density', methods=['POST'])
    def update_density():
        data = request.get_json()
        density = data.get('density')
        print(f"Updating density: {density}")
        # Add your physics calculations here
        return jsonify({
            "status": "success",
            "message": "Density updated",
            "value": density
        })

    @app.route('/electromagnetic/update_field_tensor', methods=['POST'])
    def update_field_tensor():
        data = request.get_json()
        field_tensor = data.get('field_tensor')
        print(f"Updating field tensor: {field_tensor}")
        # Add your physics calculations here
        return jsonify({
            "status": "success",
            "message": "Field tensor updated",
            "value": field_tensor
        })

    @app.route('/statistical_mechanics/update_density_matrix', methods=['POST'])
    def update_density_matrix():
        data = request.get_json()
        density_matrix = data.get('density_matrix')
        print(f"Updating density matrix: {density_matrix}")
        # Add your physics calculations here
        return jsonify({
            "status": "success",
            "message": "Density matrix updated",
            "value": density_matrix
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
