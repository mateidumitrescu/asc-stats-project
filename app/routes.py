"""This module contains the routes for the webserver."""

from flask import request, jsonify
from app import webserver, logger
from app.utilities.utils import calculate_states_mean, calculate_state_mean,\
    calculate_best5, calculate_worst5, calculate_global_mean,\
    calculate_diff_from_mean, calculate_state_diff_from_mean,\
    calculate_mean_by_category, get_jobs_helper,\
    calculate_state_mean_by_category
import json



# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Get the results of a job with the given job_id."""

    logger.info("Getting results for job_id: %s", job_id)

    if job_id not in webserver.tasks_runner.jobs:
        logger.info("Invalid job_id: %s", job_id)
        return jsonify({"status": "error", "reason": "Invalid job_id"}), 404

    if webserver.tasks_runner.jobs[job_id]["status"] == "running":
        logger.info("Job %s is still running", job_id)
        return jsonify({"status": "running"}), 200

    try:
        result_file_path = f'results/{job_id}'
        with open(result_file_path, 'r', encoding="utf-8") as file:
            result = json.load(file)
            logger.info("Job %s is done", job_id)
            return jsonify({"status": "done", "data": result}), 200
    except Exception as e:
        logger.error("Error while reading result file: %s", e)
        return jsonify({"status": "error", "reason": "Error while reading result file"}), 500

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Endpoint to calculate the mean of each state for a given question."""

    logger.info("Received request for states_mean")

    data = request.json

    job_id = webserver.tasks_runner.add_task(calculate_states_mean,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Endpoint to calculate the mean of a specific state for a given question."""

    logger.info("Received request for state_mean")

    data = request.json

    job_id = webserver.tasks_runner.add_task(calculate_state_mean,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Endpoint to calculate the best 5 states based on the mean of a given question."""

    logger.info("Received request for best5")

    data = request.json

    job_id = webserver.tasks_runner.add_task(calculate_best5,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Endpoint to calculate the worst 5 states based on the mean of a given question."""

    logger.info("Received request for worst5")

    data = request.json

    job_id = webserver.tasks_runner.add_task(calculate_worst5,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Endpoint to calculate the global mean of a given question."""

    logger.info("Received request for global_mean")

    data = request.json
    job_id = webserver.tasks_runner.add_task(calculate_global_mean,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Endpoint to calculate the difference of each state from the global mean."""

    logger.info("Received request for diff_from_mean")

    data = request.json
    job_id = webserver.tasks_runner.add_task(calculate_diff_from_mean,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Endpoint to calculate the difference of a specific state from the global mean."""

    logger.info("Received request for state_diff_from_mean")

    data = request.json
    job_id = webserver.tasks_runner.add_task(\
        calculate_state_diff_from_mean,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Endpoint to calculate the mean of each state by category."""

    logger.info("Received request for mean_by_category")

    data = request.json
    job_id = webserver.tasks_runner.add_task(calculate_mean_by_category,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Endpoint to calculate the mean of each category for a specific state."""

    logger.info("Received request for state_mean_by_category")

    data = request.json

    job_id = webserver.tasks_runner.add_task(calculate_state_mean_by_category,\
        webserver.data_ingestor.data, data)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Endpoint to get running jobs and done jobs."""

    logger.info("Received request for jobs")

    job_id = webserver.tasks_runner.add_task(get_jobs_helper,\
        webserver)

    logger.info("Job %s added to the queue", job_id)
    return jsonify({"status": "done", "job_id": job_id}), 200

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    """Endpoint to get the number of running jobs and state of the jobs."""

    logger.info("Received request for num_jobs")

    # counting only running jobs
    counter = sum(1 for job in webserver.tasks_runner.jobs.values()\
        if job["status"] == "running")

    logger.info("Number of running jobs: %s", counter)
    return jsonify({"num_jobs": counter}), 200

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """Endpoint to initiate a graceful shutdown of the webserver."""

    logger.info("Received request for graceful_shutdown")

    webserver.tasks_runner.graceful_shutdown()

    logger.info("Graceful shutdown initiated")
    return jsonify({"status": "done"}), 200

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver\
        using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += "<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
