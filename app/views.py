import os
import subprocess
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Set up a logger with a file handler and a formatter
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Define a list of processes to monitor
processes = [
    {
        'name': 'goiu_v3.py',
        'path': '/home/novogad/payzocard_bot_forward/goiu_v3.py',
        'log': '/home/novogad/payzocard_bot_forward/goiu_v3.log'
    },
    {
        'name': 'copn.py',
        'path': '/home/novogad/payzocard_bot_forward/copn.py',
        'log': '/home/novogad/payzocard_bot_forward/copn.log' 
    },
    {
        'name': 'main.py',
        'path': '/home/novogad/wallester_bot/bot_api/telegram-bot-payment/main.py',
        'log': None
    },
    {
        'name': 'app.py',
        'path': '/home/novogad/novoapi/app.py',
        'log': None
    },
    {
        'name': 'main.py',
        'path': '/home/novogad/otpbotcode/main.py',
        'log': None
    }
]

# Define a function to check the status of a process by its name
def check_process_status(process_name):
    # Use ps command to get the process information
    ps = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE).communicate()[0]
    # Decode the output and split it by lines
    processes = ps.decode().split('\n')
    # Loop through the processes and look for the matching name
    for process in processes:
        if process_name in process:
            # If found, return the process information as a dictionary
            fields = process.split()
            return {
                'pid': fields[1],
                'user': fields[0],
                'cpu': fields[2],
                'mem': fields[3],
                'command': fields[-1]
            }
    # If not found, return None
    return None

# Define a function to read the last line of a log file
def read_last_log_line(log_file):
    # Open the log file in read mode
    with open(log_file, 'r') as f:
        # Seek to the end of the file
        f.seek(0, os.SEEK_END)
        # Get the file size in bytes
        fsize = f.tell()
        # Loop backwards until a newline is found or the start of the file is reached
        while fsize > 0:
            fsize -= 1
            f.seek(fsize)
            ch = f.read(1)
            if ch == '\n':
                break
        # Return the last line of the file
        return f.readline()

# Define an api view function to handle the request for the status of the processes
@api_view(['GET'])
def get_process_status(request):
    # Indent the code inside the function by four spaces
    status_list = []
    # Loop through the processes to monitor
    for process in processes:
        # Create an empty dictionary to store the status of the current process
        status_dict = {}
        # Check the status of the process by its name
        status = check_process_status(process['name'])
        # If the status is not None, it means the process is running
        if status:
            # Check if the process has a log file
            if process['log']:
                # Read the last line of the log file
                last_log_line = read_last_log_line(process['log'])
                # Check if the last line contains an error message
                if 'error' in last_log_line.lower():
                    # Log an error message with the process name and the log line
                    logger.error(f"{process['name']} is running with error: {last_log_line}")
                    # Add an entry to the status dictionary with the process name, error log and status code 2 (run with error)
                    status_dict[process['name']] = 'running with error'
                    status_dict['error_log'] = last_log_line.strip()
                    status_dict['status_code'] = 2
                else:
                    # Log an info message with the process name and status code 1 (running)
                    logger.info(f"{process['name']} is running")
                    # Add an entry to the status dictionary with the process name, error log and status code 1 (running)
                    status_dict[process['name']] = 'running'
                    status_dict['error_log'] = last_log_line.strip()
                    status_dict['status_code'] = 1
            else:
                # Log an info message with the process name and status code 1 (running)
                logger.info(f"{process['name']} is running")
                # Add an entry to the status dictionary with the process name, no log and status code 1 (running)
                status_dict[process['name']] = 'running'
                status_dict['error_log'] = 'No log'
                status_dict['status_code'] = 1
            
        # If the status is None, it means the process is not running or stopped with error
        else:
            # Log a warning message with the process name and path
            logger.warning(f"{process['name']} stopped or not running at {process['path']}")
            # Add an entry to the status dictionary with the process name, path and status code 3 (down)
            status_dict[process['name']] = 'down'
            status_dict['path'] = process['path']
            status_dict['status_code'] = 3
        
        # Append the status dictionary to the status list
        status_list.append(status_dict)
    
    # Return a response with the status list as data and a 200 OK status code 
    return Response(data=status_list, status=200)
