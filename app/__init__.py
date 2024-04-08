"""Initializing the Flask app and set up the logger."""

from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.config.logger_config import setup_logger
import os

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

if not os.path.exists('results'):
    os.makedirs('results')

webserver.job_counter = 1

logger = setup_logger()

from app import routes
