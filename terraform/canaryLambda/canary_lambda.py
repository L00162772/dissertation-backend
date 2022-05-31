import boto3
import os

global_accelerator_region = "us-west-2"
base_application_dns = "atu-dissertation.com."

print("In canary lambda - 123")

client = boto3.client('globalaccelerator', region_name=global_accelerator_region)

aws_region = os.environ['REGION']
application_type = os.environ['APPLICATION_TYPE']
elbv2_client = boto3.client('elbv2',  region_name=aws_region)


def lambda_handler(event, context):
    print(f"event:{event}")

    test_run_status = event['detail']['test-run-status']
    print(f"test_run_status:{test_run_status}")
   
    list_accelerators_response = client.list_accelerators()
    print(f"list_accelerators_response: {list_accelerators_response}")

    accelerator_arn = _get_accelerator_arn(list_accelerators_response)
    print(f"accelerator_arn:{accelerator_arn}")

    listener_arn = _get_listener_arn(accelerator_arn)
    print(f"listener_arn:{listener_arn}")

    if test_run_status.lower() == "failed":
        print("Test failed - remove region from global accelerator")
        _delete_region_from_global_accelerator(listener_arn)
    else:
        print("Test Passed - verify region is part of global accelerator")
        _add_region_to_global_accelerator(listener_arn)
  
def _get_listener_arn(accelerator_arn) -> str:
    list_listeners_response = client.list_listeners( AcceleratorArn=accelerator_arn)
    print(f"list_listeners_response: {list_listeners_response}")
    print(f"type: {type(list_listeners_response)}")
    if len(list_listeners_response['Listeners']) <= 0:
        print(f"No listeners returned")

    listener_arn = list_listeners_response['Listeners'][0]['ListenerArn']
    return listener_arn

def _get_accelerator_arn(list_accelerators_response) -> str:
    accelerator_arn = ''
    accelerator_dns = ''
    for accelerator in list_accelerators_response['Accelerators']:
        print(f"accelerator: {accelerator}")
        temp_accelerator_arn = accelerator['AcceleratorArn']
        print(f"temp_accelerator_arn: {temp_accelerator_arn}")

        tags_for_resource_response = client.list_tags_for_resource(ResourceArn=temp_accelerator_arn)
        print(f"tags_for_resource_response: {tags_for_resource_response}")

        has_application_type_tag = False
        for tag in tags_for_resource_response['Tags']:
            print(f"tag: {tag}")
            key = tag['Key']
            value = tag['Value']
            if key == 'Name' and value.lower() == application_type:
                has_application_type_tag = True
                accelerator_arn = temp_accelerator_arn
                print(f"accelerator_arn: {accelerator_arn}")
                accelerator_dns = accelerator['DnsName']
                print(f"accelerator_dns: {accelerator_dns}")

            print(f"has_application_type_tag: {has_application_type_tag}")

        if has_application_type_tag:
            break
    
    return accelerator_arn

def _delete_region_from_global_accelerator(listener_arn):
    list_endpoint_groups_response = client.list_endpoint_groups(ListenerArn=listener_arn)
    print(f"list_endpoint_groups_response:{list_endpoint_groups_response}")
    for endpoint_group in list_endpoint_groups_response['EndpointGroups']:
        print(f"endpoint_group:{endpoint_group}")
        endpoint_group_region = endpoint_group['EndpointGroupRegion']
        print(f"endpoint_group_region:'{endpoint_group_region}', aws_region:'{aws_region}'")
        if endpoint_group_region.lower() == aws_region.lower():
            print(f"Deleting endpoint group for region {aws_region}")
            endpoint_group_arn = endpoint_group['EndpointGroupArn']
            print(f"endpoint_group_arn:{endpoint_group_arn}")
            
            delete_endpoint_group_response = client.delete_endpoint_group(EndpointGroupArn=endpoint_group_arn)
            print(f"delete_endpoint_group_response:{delete_endpoint_group_response}")

def _add_region_to_global_accelerator(listener_arn):
    load_balancer_arn = _get_load_balancer_arn()
    print(f"load_balancer_arn: {load_balancer_arn}")

    already_has_listener_for_region = False
    list_endpoint_groups_response = client.list_endpoint_groups(ListenerArn=listener_arn)
    print(f"list_endpoint_groups_response:{list_endpoint_groups_response}")
    for endpoint_group in list_endpoint_groups_response['EndpointGroups']:
        print(f"endpoint_group:{endpoint_group}")
        endpoint_group_region = endpoint_group['EndpointGroupRegion']
        print(f"endpoint_group_region:'{endpoint_group_region}', aws_region:'{aws_region}'")
        if endpoint_group_region.lower() == aws_region.lower():
            already_has_listener_for_region = True


    if not already_has_listener_for_region:
        print("Creating listener - no listener exists for this region")
        create_endpoint_group_response = client.create_endpoint_group(
            ListenerArn=listener_arn,
            EndpointGroupRegion=aws_region,
            EndpointConfigurations=[
                {
                    'EndpointId': load_balancer_arn,
                    'Weight': 123,
                    'ClientIPPreservationEnabled': False
                },
            ],
            HealthCheckPort=80,
            HealthCheckProtocol='HTTP',
            HealthCheckPath='/index.html',
            HealthCheckIntervalSeconds=10,
            ThresholdCount=3,
            IdempotencyToken='string',
        )
        print(f"create_endpoint_group_response:{create_endpoint_group_response}")            
    else:
        print("Not Creating listener as it already exists")

def _get_load_balancer_arn():
    describe_load_balancers_response = elbv2_client.describe_load_balancers()
    print(f"describe_load_balancers_response:{describe_load_balancers_response}")
    load_balancer_arn = ''
    for load_balancer in describe_load_balancers_response['LoadBalancers']:
        print(f"load_balancer:{load_balancer}")

        load_balancer_name = load_balancer['LoadBalancerName']
        print(f"load_balancer_name:{load_balancer_name}")

        if load_balancer_name.startswith(application_type):
            load_balancer_arn = load_balancer['LoadBalancerArn']
    
    return load_balancer_arn