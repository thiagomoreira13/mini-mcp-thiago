from flask import Flask, request, jsonify, render_template
import requests
import uuid
import time
import json


app = Flask(__name__)


# In-memory data stores
registered_servers = {}
saved_experiments = {}


@app.route('/register-server', methods=['POST'])
def register_server():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing server URL'}), 400


    server_id = str(uuid.uuid4())
    registered_servers[server_id] = url
    return jsonify({'server_id': server_id})


@app.route('/tools', methods=['GET'])
def get_tools():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400


    try:
        response = requests.get(f"{url}/tools/list")
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/run-test', methods=['POST'])
def run_test():
    data = request.json
    url = data.get('url')
    tool_name = data.get('tool_name')
    input_args = data.get('input', {})
    iterations = int(data.get('iterations', 1))


    if not url or not tool_name:
        return jsonify({'error': 'Missing url or tool_name'}), 400


    results = []
    for _ in range(iterations):
        try:
            start = time.time()
            response = requests.post(f"{url}/tools/call", json={
            "tool_name": tool_name,
            "input": input_args
            })
            duration = time.time() - start
            results.append({
            "status_code": response.status_code,
            "response": response.json() if response.ok else response.text,
            "duration_ms": int(duration * 1000)
            })
        except Exception as e:
            results.append({
            "error": str(e),
            "duration_ms": 0
            })


    experiment_id = str(uuid.uuid4())
    saved_experiments[experiment_id] = results


    return jsonify({
        "experiment_id": experiment_id,
        "results": results
        })


@app.route('/results/<experiment_id>', methods=['GET'])
def get_results(experiment_id):
    results = saved_experiments.get(experiment_id)
    if not results:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(results)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
