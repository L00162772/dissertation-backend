import os
import boto3
import time 

aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']

dynamodb_region = "us-east-1"
dynamodb_table_name = "users"

print("In setup DynamoDB")

def _create_dynamodb_table(boto3_client, table_name, region, streams_enabled = False):
    print(f"1. _create_dynamodb_table table_name:{table_name}")
    table_already_exists = False
    try:
        describe_table_response = boto3_client.describe_table(TableName=dynamodb_table_name)
        print(f"3. _create_dynamodb_table. describe_table_response: {describe_table_response}")
        table_already_exists = True   
    except:
        table_already_exists = False

    print(f"3. table_already_exists:{table_already_exists} ")
    if table_already_exists:
        return 
        
    create_table_response = boto3_client.create_table(TableName=table_name,
        AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        }
    ], 
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    BillingMode='PAY_PER_REQUEST',
    StreamSpecification={
        'StreamEnabled': streams_enabled,
        'StreamViewType': 'NEW_AND_OLD_IMAGES'
    },)
    print(f"create_table_response: {create_table_response}")

    _wait_until_table_ready(boto3_client, table_name, region)

def _wait_until_table_ready(boto3_client, table_name, region):         
    table_status = "empty"
    count = 0
    while table_status.lower() != "active" and count < 100:
        if count > 0:
            sleep_time = 5 + count
            print(f" Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
        
        count += 1
        try:
            describe_table_response = boto3_client.describe_table(TableName=table_name)
            print(f"describe_table_response: {describe_table_response}")
            table_status = describe_table_response['Table']['TableStatus']
            print(f"table_status: {table_status}")
        except Exception as e:
            print(f"Unable to find table. Exception: {e}. region: {region}")
            table_status = "deleted"

client = boto3.client('dynamodb',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=dynamodb_region)

region_client = boto3.client('dynamodb',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=aws_region)


list_tables_response = client.list_tables()
print(f"list_tables_response: {list_tables_response}")

distribution_id = ''
base_table_already_created = False
for table_name in list_tables_response['TableNames']:
    print(f"table_name: {table_name}")

    if table_name.lower() == dynamodb_table_name.lower():
        base_table_already_created = True
        break

print(f"base_table_already_created:{base_table_already_created}")
# If the table is not already created then create it
if not base_table_already_created and aws_region.lower() == dynamodb_region:
    print("Creating initial table")
    _create_dynamodb_table(client, dynamodb_table_name, dynamodb_region, True)

# If not in the dynamodb region - check if a replica exists, if not then create it
if aws_region.lower() != dynamodb_region:
    print(f"1. aws_region:{aws_region}, dynamodb_region:{dynamodb_region}")

    replica_already_created = False
    try:
        describe_table_response = client.describe_table(TableName=dynamodb_table_name)
        print(f"2. describe_table_response: {describe_table_response}")
        if "Replicas" in describe_table_response['Table']:
            for replica in describe_table_response['Table']['Replicas']:
                print(f"2.1. replica: {replica}")
                replica_region = replica['RegionName']
                if replica_region.lower() == aws_region.lower():
                    replica_already_created = True
                    break        
    except:
        replica_already_created = False

    print(f"replica_already_created:{replica_already_created}")

    if not replica_already_created:
            print("3. Replica is not already created - creating")
            _wait_until_table_ready(client, dynamodb_table_name, aws_region)
            update_table_response = client.update_table(
                TableName=dynamodb_table_name,
                ReplicaUpdates = 
                [
                    {
                    "Create": {
                        "RegionName": aws_region
                    }
                    }
                ]
            )
            print(f"4. update_table_response: {update_table_response}")



