import requests
import json
import time
import threading


# Define the pulse sending URL
url = ""

# Heartbeat control variable
variable_parameter = True

# Pulse thread
pulse_thread = None

# 0
def setUrl(url_):
    '''
    ----------------------------------------------------------
    Function to set a URL for pulse sending

    Parameters:
        url_ (str): URL for pulse sending
    ----------------------------------------------------------
    '''

    global url
    url = url_


# 1
def sendPulse(name, description, additional_info, show_response):
    '''
    ----------------------------------------------------------
    Function to send a pulse to the server

    Parameters:
        name (str): process name
        description (str): process description
        additional_info (str) (optional): additional process data
        show_response (bool) (optional): show server response
    ----------------------------------------------------------
    '''

    try:
        payload = json.dumps({
            "processName": f"{name}",
            "processDescription": f"{description}",
            "additionalData": f"{additional_info}"
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)

    except Exception as e:
        print('\n*** Error sending pulse! *** >', e)

    finally:
        try:
            if show_response:
                print(f'>>> Heartbeat response: {response.status_code} <<<')
            pass
        except:
            pass 


# 2
def pulse(interval, name, description, additional_info, show_response, show_logs):
    '''
    ----------------------------------------------------------
    Function to send a pulse to the server at regular intervals

    Parameters:
        interval (int): time between pulses (in seconds)
        name (str): process name
        description (str): process description
        additional_info (str) (optional): additional process data
        show_response (bool) (optional): show server response
        show_logs (bool) (optional): show log messages
    ----------------------------------------------------------
    '''

    if show_logs:
        print('>>> Heartbeat thread has started. <<<')
    
    while variable_parameter:
        sendPulse(name, description, additional_info, show_response)

        # If the variable_parameter is False, break the loop
        for _ in range(interval):
            if not variable_parameter:
                break # break the loop
            time.sleep(1)

    if show_logs:
        print('>>> Heartbeat thread has ended. <<<')


# 3
def heartbeat(interval = 600, name = '', description = '', additional_info = '', show_response = False, show_logs = False):
    '''
    ----------------------------------------------------------
    Function to start the heartbeat

    Parameters:
        interval (int): time between pulses (in seconds)
        name (str): process name
        description (str): process description
        additional_info (str) (optional): additional process data
        show_response (bool) (optional): show server response
        show_logs (bool) (optional): show log messages
    ----------------------------------------------------------
    '''
    
    global variable_parameter, pulse_thread

    # Set variable_parameter to True
    variable_parameter = True

    try:
        # If there is already a thread running, wait for it to finish
        if pulse_thread is not None:
            pulse_thread.join(timeout=1.0)

        # Start the pulse thread
        pulse_thread = threading.Thread(target=pulse, args=(interval, name, description, additional_info, show_response, show_logs))
        pulse_thread.start()

    except Exception as e:
        print('*** Error in heartbeat thread! *** > ', e)


# 4
def killHeartbeat():
    '''
    ----------------------------------------------------------
    Function to stop the heartbeat
    ----------------------------------------------------------
    '''

    global variable_parameter, pulse_thread
    variable_parameter = False
    time.sleep(1)

    # Check the status of the thread
    if pulse_thread is not None and pulse_thread.is_alive():
        print('>>> Heartbeat thread is still running. <<<')
    else:
        print('>>> Heartbeat thread has ended. <<<')
