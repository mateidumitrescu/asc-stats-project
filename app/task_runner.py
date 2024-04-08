"""This module contains the ThreadPool class which
is used to create a thread pool to handle tasks concurrently."""

from queue import Queue, Empty
from threading import Thread, Event, Lock
import os
import shutil
import json

class ThreadPool:
    """Class used for creating a thread pool to handle tasks concurrently"""
    def __init__(self):
        # initializing needed attributes
        self.task_queue = Queue() # storing the tasks
        self.shutdown_event = Event() # used to signal the threads to shutdown
        self.jobs = {}  # job id's and their status
        self.job_counter = 1 # used to generate job id's
        self.lock = Lock() # used for controlling access to job_counter
        self.workers = [] # actual worker threads

        # number of threads
        num_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count()))
        # worker threads
        for _ in range(num_threads):
            worker = TaskRunner(self.task_queue, self.shutdown_event, self.update_job_status)
            worker.start()
            self.workers.append(worker)

    def add_task(self, task, *args, **kwargs):
        """Method to add a task to the task queue and return the job id for tracking"""
        # using lock to prevent race conditions when updating job_counter
        with self.lock:
            job_id = "job_id_" + str(self.job_counter)
            self.jobs[job_id] = {"status": "running"}
            self.job_counter += 1
        # add the task to the task queue
        self.task_queue.put((job_id, task, args, kwargs))
        return job_id  # Return job_id for tracking

    def update_job_status(self, job_id, status, result=None):
        """Method to update the status of a job"""
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['status'] = status
                if result is not None:
                    self.jobs[job_id]['result'] = result

    def graceful_shutdown(self):
        """Method to shutdown the thread pool"""
        self.shutdown_event.set()
        for worker in self.workers:
            worker.join()
        self.task_queue.join()

class TaskRunner(Thread):
    """Class used for running tasks in a separate thread"""
    def __init__(self, task_queue: Queue, shutdown_event: Event, update_status_callback):
        super().__init__()
        self.task_queue = task_queue
        self.shutdown_event = shutdown_event
        self.update_status = update_status_callback

    def run(self):
        """Method to run the tasks in the task queue"""
        while not self.shutdown_event.is_set():
            try:
                # setting a timeout to avoid blocking indefinitely and wait for shutdown event
                # another alternative is to use a 'poison pill' to signal the threads to shutdown
                job_id, task, args, kwargs = self.task_queue.get(timeout=1)
                result = task(*args, **kwargs)
                with open('results/' + job_id, 'w', encoding="utf-8") as file:
                    file.write(json.dumps(result))
                # updating the status of the job
                self.update_status(job_id, "done", result)
                self.task_queue.task_done()
            except Empty: # raised when the queue is empty
                continue
