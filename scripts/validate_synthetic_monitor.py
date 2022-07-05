import os
import boto3
import botocore
import time
aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']

print("In validate Synthetic Monitor")

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
    print("Start - sleeping for 3 minutes")
    # time.sleep(60 * 3)
    time.sleep(3)
    print("End - sleeping for 3 minutes")

    canary_runs = client.get_canary_runs(Name=synthetic_monitor_name)
    print(f"canary_runs:{canary_runs}")

    passed_count = 0
    failed_count = 0
    for canary_run in canary_runs['CanaryRuns']:
        print(f"canary_run: {canary_run}")
        state = canary_run['Status']['State']
        print(f"state: {state}")
        if state.lower() == 'passed':
            passed_count += 1
        else:
            failed_count += 1
    
    print(f"passed_count:{passed_count}, failed_count:{failed_count}")

    if passed_count <= failed_count:
        print("Errors have been logged - fail workflow")
        raise("Exception checking Synthetic monitors")
