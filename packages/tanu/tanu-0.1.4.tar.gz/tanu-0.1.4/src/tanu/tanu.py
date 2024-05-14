"""
    Copyright (C) 2024  chocolate-icecream

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import inspect
import logging

import threading
import queue
import uuid
import traceback
from enum import Enum
import hashlib
import os
import pika

from pydantic import BaseModel, create_model, Field, ConfigDict
from .utils import object_encoder_decoder


# Set up basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# Define possible statuses for task processing
class StatusEnum(str, Enum):
    DONE = "done"
    ERROR = "error"
    RUNNING = "running"
    REQUESTED = "requested"

# Data model for request letters
class RequestLetter(BaseModel):
    job_id: str
    result_queue_name: str
    command: str
    params: dict
    units: dict
    encoded: dict = {}

# Data model for response letters
class ResponseLetter(BaseModel):
    job_id: str
    status: StatusEnum
    request: dict
    result: dict
    units: dict
    encoded: dict = {}

# Function to apply custom encoding to data items
def apply_encoder(encoded_dict, item, serialized_key):
    """Apply encoding to non-primitive types using registered encoders."""
    if isinstance(item, (int, float, str, list, set)):
        return None
    if isinstance(item, dict):
        for key, value in item.items():
            encoded_value = apply_encoder(encoded_dict, value, serialized_key=serialized_key + f"/{key}")
            if encoded_value:
                item[key] = encoded_value
        return None
    for encoder_name, encoder_method in object_encoder_decoder.encoders.items():
        encoded_value = encoder_method(item)
        if encoded_value:
            if encoder_name not in encoded_dict:
                encoded_dict[encoder_name] = []
            encoded_dict[encoder_name].append(serialized_key)
            return encoded_value
    raise Exception(f"Cannot perform proper encoding on {serialized_key}: {type(item)}")

# Function to apply custom decoding to data items
def apply_decoder(letter):
    """Apply decoding to encoded data items using registered decoders."""
    for name, targets in letter.encoded.items():
        decoder = object_encoder_decoder.decoders[name]
        for serialized_key in targets:
            keys = serialized_key.split("/")
            target_dict = getattr(letter, keys[0])
            for key in keys[1:-1]:
                target_dict = target_dict[key]
            target_dict[keys[-1]] = decoder(target_dict[keys[-1]])

class Tanuki:
    def __init__(self, worker_name, host=None, port=None, callback_func=None, accept_previous_job=True):
        """Initialize the Tanuki worker with basic configurations."""
        self.worker_name = worker_name
        if host is None:
            url = os.getenv("TANU_RABBITMQ_URL")
            if len(url) == 0:
                self.host = "localhost"
                self.port = port if port else 5672
            else:
                self.host = ":".join(url.split(":")[:-1])
                self.port = port if port else int(url.split(":")[-1])
        else:
            self.host = host
            self.port = port if port else 5672
        self.callback_func = callback_func
        self.accept_previous_job = accept_previous_job
        self.result_queues = {}
        self.units = {}
        self.unique_identifier = self.generate_unique_identifier()
        self.prepare_task_queue()
        self.start_result_retrieve_thread()

    def prepare_task_queue(self):
        """Prepare the task queue by connecting to the message broker."""
        self.task_connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        self.task_channel = self.task_connection.channel()
        self.task_channel.queue_declare(queue=self.task_queue_name, durable=True)

    def start_result_retrieve_thread(self):
        """Start a separate thread to handle result retrieval."""
        t = threading.Thread(target=self.start_consumer)
        t.daemon = True
        t.start()

    def start_consumer(self):
        """Continuously consume results from the result queue."""
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.result_queue_name)
        channel.basic_consume(queue=self.result_queue_name, auto_ack=True, on_message_callback=self.on_result_received)
        channel.start_consuming()

    def on_result_received(self, ch, method, properties, body):
        """Handle received results and trigger callback if set."""
        try:
            response = ResponseLetter.parse_raw(body)
            apply_decoder(response)
            if response.job_id in self.result_queues:
                self.result_queues[response.job_id].put_nowait(response)
            elif not self.accept_previous_job:
                raise Exception("Received a previous job")
            if self.callback_func:
                self.callback_func(response)
        except Exception as e:
            logger.error(f"Error processing result: {traceback.format_exc()}")

    def send(self, payload):
        """Send a task payload to the task queue."""
        payload = payload.copy()
        job_id = uuid.uuid4().hex
        payload["job_id"] = job_id
        payload["units"] = self.units
        payload["result_queue_name"] = self.result_queue_name
        payload["encoded"] = {}
        apply_encoder(payload["encoded"], payload["params"], "params")
        request = RequestLetter(**payload)
        message = request.json()
        try:
            self.task_channel.basic_publish(exchange="", routing_key=self.task_queue_name, body=message, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))
        except (pika.exceptions.StreamLostError, pika.exceptions.ChannelWrongStateError):
            self.close_task_connection()
            self.prepare_task_queue()
            self.task_channel.basic_publish(exchange="", routing_key=self.task_queue_name, body=message, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))

        job = TanukiJob(self, job_id)
        self.result_queues[job_id] = job.queue
        return job

    def wait_for_result(self, job_id):
        """Block until a result is available for the given job ID."""
        assert job_id in self.result_queues
        return self.result_queues[job_id].get()

    def __call__(self, command, **kwargs):
        """Shortcut method to send a command and wait for the result."""
        job = self.call(command, params=kwargs)
        return job.wait_till_done()

    def call(self, command, params=None):
        """Prepare and send a command payload."""
        if params is None:
            params = {}
        payload = {"command": command, "params": params}
        return self.send(payload)

    def generate_job_id(self):
        """Generate a unique job ID."""
        return uuid.uuid4().hex

    def generate_unique_identifier(self):
        """Generate a unique identifier for this instance."""
        unique_str = str(uuid.getnode()) + os.path.abspath(__file__)
        hasher = hashlib.sha1(unique_str.encode())
        return uuid.UUID(hasher.hexdigest()[:32])

    def close_task_connection(self):
        """Close the messaging connections gracefully."""
        try:
            self.task_channel.close()
        except pika.exceptions.ChannelWrongStateError:
            pass
        try:
            self.task_connection.close()
        except pika.exceptions.ConnectionWrongStateError:
            pass

    @property
    def task_queue_name(self):
        """Construct and return the task queue name based on worker name."""
        return f"task_{self.worker_name}"

    @property
    def result_queue_name(self):
        """Construct and return the result queue name based on worker name and unique identifier."""
        return f"result_{self.worker_name}_{self.unique_identifier}"


class TanukiJob:
    """Handles the lifecycle of a job including waiting for and retrieving results."""

    def __init__(self, parent, job_id):
        self.parent = parent
        self.job_id = job_id
        self.queue = queue.Queue()
        self.status = StatusEnum.REQUESTED
        self.response = None
    
    def wait_till_done(self):
        """Wait for the job to be completed or errored out and return the result."""
        while True:
            self.response = self.queue.get()
            if self.response.status in [StatusEnum.DONE, StatusEnum.ERROR]:
                break
        del self.parent.result_queues[self.job_id]
        del self.queue
        if self.response.status == StatusEnum.ERROR:
            raise Exception(self.response.result["msg"])

        return self.response.result

class TanukiResponseConnection:
    """Manages the communication of results back to the requester."""

    def __init__(self, request: RequestLetter = None, units=None):
        self.request = request
        self.units = units if units else {}
        self.connect()

    @classmethod
    def send_error(cls, request: RequestLetter, msg: str):
        """Send an error message back to the requester."""
        logger.error(msg)
        connection = TanukiResponseConnection(request)
        connection.send_status(StatusEnum.ERROR, msg)
        connection.close()
    
    def connect(self):
        """Establish a connection to the message broker."""
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
    
    def set_request(self, request: RequestLetter):
        """Set the request details for sending responses."""
        self.request = request
    
    def send(self, status: StatusEnum, result: dict):
        """Send a status update or result back to the requester."""
        assert self.request, "Request must be set before sending data."
        
        request_dict = {"command": self.request.command, "params": self.request.params}
        encoded_dict = {}
        apply_encoder(encoded_dict, self.request.params, "request/params")
        apply_encoder(encoded_dict, result, "result")
        response = ResponseLetter(job_id=self.request.job_id, status=status, request=request_dict, result=result, units=self.units)
        message = response.json()

        try:
            self.channel.queue_declare(queue=self.request.result_queue_name)
            self.channel.basic_publish(exchange="", routing_key=self.request.result_queue_name, body=message)
        except pika.exceptions.StreamLostError:
            logger.debug("Stream Lost Error. Try reconnection...")
            self.close()
            self.connect()
            self.channel.queue_declare(queue=self.request.result_queue_name)
            self.channel.basic_publish(exchange="", routing_key=self.request.result_queue_name, body=message)

    def send_status(self, status: StatusEnum, msg: str):
        """Send a simple status message."""
        self.send(status, {"msg": msg})
            
    def close(self):
        """Close the messaging connections gracefully."""
        try:
            self.channel.close()
        except pika.exceptions.ChannelWrongStateError:
            pass
        try:
            self.connection.close()
        except pika.exceptions.ConnectionWrongStateError:
            pass

class TanukiWorker:
    """Defines a worker that can execute commands based on requests received through a message queue."""

    def __init__(self, name: str, auth: str = ""):
        self.name = name
        self.auth = auth
        self.command_dict = {}
        self.units = {}
    
    def run(self):
        """Start consuming tasks from the queue."""
        queue_name = f"task_{self.name}"
        self.connection_for_task_queue = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.base_response_connection = TanukiResponseConnection(units=self.units)
        channel = self.connection_for_task_queue.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=self._call_command)
        logger.info(f"{self.name} starts running...")
        channel.start_consuming()

    def _call_command(self, ch_req, method, properties, body):
        """Process incoming command requests."""
        try:
            request = RequestLetter.parse_raw(body)
            if request.command not in self.command_dict:
                TanukiResponseConnection.send_error(request, f"Tanuki Worker {self.name} cannot recognize '{request.command}'.")
                ch_req.basic_ack(delivery_tag=method.delivery_tag)
                return
        except Exception as e:
            logger.error(traceback.format_exc())
            ch_req.basic_ack(delivery_tag=method.delivery_tag)
            return

        try:
            if self.command_dict[request.command]["multi_threading"]:
                t = threading.Thread(target=self._perform_registered_command_for_multi_threading,
                                    kwargs={"request": request, "multi_threading": True,
                                            "pool_size": self.command_dict[request.command]["pool_size"],
                                            "ch_req": ch_req,
                                            "delivery_tag": method.delivery_tag})
                t.daemon = True
                t.start()
            else:
                self._perform_registered_command(self.base_response_connection, request)
        except Exception as e:
            TanukiResponseConnection.send_error(request, traceback.format_exc())
        finally:
            if not self.command_dict[request.command]["multi_threading"]:
                ch_req.basic_ack(delivery_tag=method.delivery_tag)

    def _perform_registered_command(self, connection: TanukiResponseConnection, request: RequestLetter):
        """Execute a registered command."""
        apply_decoder(request)
        connection.set_request(request)
        func = self.command_dict[request.command]["func"]
        model = self.command_dict[request.command]["pydantic_model"]
        params = model(**request.params).dict()
        logger.debug(f"Received request ({request.command}): {params}")
        result = func(**params)
        if isinstance(result, dict):
            connection.send(StatusEnum.DONE, result)
        else:
            logger.error(f"{request.command} on {self.name} returns an incorrect result {result} with type {type(result)}.")
            connection.send_status(StatusEnum.ERROR, f"{request.command} on {self.name} returns an incorrect result {result} with type {type(result)}.")
            

    def _perform_registered_command_for_multi_threading(self, request: RequestLetter, ch_req, delivery_tag):
        """Execute a registered command in a separate thread."""
        connection = TanukiResponseConnection(request, units=self.units)
        try:
            self._perform_registered_command(request)
        finally:
            connection.close()
            self._ack_message(ch_req, delivery_tag)

    def _ack_message(self, channel, delivery_tag):
        """Acknowledge the message processing completion for a specific delivery tag."""
        self._connection_for_task_queue.add_callback_threadsafe(lambda: channel.basic_ack(delivery_tag=delivery_tag))
    
    def command(self, name, multi_threading_pool_size=0):
        """Decorator to register a function as a command that can be executed in response to requests."""
        def named_wrapper(func):
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            assert name not in self.command_dict, "Command already registered."
            model = create_pydantic_model_for_user_defined_func(func)
            self.command_dict[name] = {"func": func, "pydantic_model": model,
                                        "multi_threading": multi_threading_pool_size > 0,
                                        "pool_size": multi_threading_pool_size}
            return wrapper
        return named_wrapper

def create_pydantic_model_for_user_defined_func(func):
    """Dynamically create a Pydantic model based on the function's signature."""
    sig = inspect.signature(func)
    fields = {}
    for name, param in sig.parameters.items():
        field_info_dict = {"default": param.default} if param.default is not inspect.Parameter.empty else {}
        fields[name] = (param.annotation, Field(**field_info_dict))
    dynamic_model = create_model(func.__name__ + "Model", **fields, __config__=ConfigDict(arbitrary_types_allowed=True))
    return dynamic_model