import os
import boto3

aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']
add_accelerator_for_region = os.environ['ADD_ACCELERATOR_FOR_REGION']

global_accelerator_region = "us-west-2"

base_application_dns = "atu-dissertation.com."

print("In configure global accelerator")

client = boto3.client('globalaccelerator',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=global_accelerator_region)

elbv2_client = boto3.client('elbv2',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=aws_region)

list_accelerators_response = client.list_accelerators()
print(f"list_accelerators_response: {list_accelerators_response}")

distribution_id = ''
has_application_type_tag = False
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
            accelerator_dns = accelerator['DnsName']
            print(f"accelerator_dns: {accelerator_dns}")

        print(f"has_application_type_tag: {has_application_type_tag}")

    if has_application_type_tag:
        break

list_listeners_response = client.list_listeners( AcceleratorArn=accelerator_arn)
print(f"list_listeners_response: {list_listeners_response}")
print(f"type: {type(list_listeners_response)}")
if len(list_listeners_response['Listeners']) <= 0:
    print(f"No listeners returned")

listenerARN = list_listeners_response['Listeners'][0]['ListenerArn']

describe_load_balancers_response = elbv2_client.describe_load_balancers()
print(f"describe_load_balancers_response:{describe_load_balancers_response}")
load_balancer_arn = ''
for load_balancer in describe_load_balancers_response['LoadBalancers']:
    print(f"load_balancer:{load_balancer}")

    load_balancer_name = load_balancer['LoadBalancerName']
    print(f"load_balancer_name:{load_balancer_name}")

    if load_balancer_name.startswith(application_type):
        load_balancer_arn = load_balancer['LoadBalancerArn']

print(f"add_accelerator_for_region:{add_accelerator_for_region}")
if add_accelerator_for_region.lower() == "true":
    print("Adding a global accelerator")
    create_endpoint_group_response = client.create_endpoint_group(
        ListenerArn=listenerARN,
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
    print("Deleting a global accelerator endpoint group")
    list_endpoint_groups_response = client.list_endpoint_groups(ListenerArn=listenerARN)
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

