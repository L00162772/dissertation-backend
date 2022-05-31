import os
import boto3
import botocore

aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']
start_synthetic_monitor = os.environ['START_SYNTHETIC_MONITOR']


print("In configure Synthetic Monitor")

client = boto3.client('synthetics',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=aws_region)


synthetic_monitor_name = f'{application_type}_canary'
print(f"synthetic_monitor_name:{synthetic_monitor_name}")

canary_state = None
try:
    get_canary_response = client.get_canary(Name=synthetic_monitor_name)
    print(f"get_canary_response:{get_canary_response}")

    canary_state = get_canary_response['Canary']['Status']['State']
    print(f"canary_state:{canary_state}")
except:
    print("An exception has occured - perhaps canary does not exist.")

if canary_state is not None:
    print(f"start_synthetic_monitor:{start_synthetic_monitor}")
    if start_synthetic_monitor.lower() == "true":
        if canary_state == 'STOPPED' or canary_state == 'READY':
            print("Starting the synthetic monitor")
            start_canary_response = client.start_canary(Name=synthetic_monitor_name)
            print(f"start_canary_response:{start_canary_response}")
    else:
        if canary_state == 'RUNNING':
            print("Stopping the synthetic monitor")
            stop_canary_response = client.stop_canary(Name=synthetic_monitor_name)
            print(f"stop_canary_response:{stop_canary_response}")