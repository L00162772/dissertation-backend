import os
import boto3

aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']

dynamodb_region = "us-east-1"
dynamodb_table_name = "users"

print("In setup DynamoDB")

def _create_dynamodb_table(boto3_client, table_name, streams_enabled = False):
    create_table_response = boto3_client.create_table(TableName=table_name,
        AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
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
table_already_created = False
for table_name in list_tables_response['TableNames']:
    print(f"table_name: {table_name}")

    if table_name.lower() == dynamodb_table_name.lower():
        table_already_created = True
        break


# If the table is not already created then create it

if not table_already_created:
    _create_dynamodb_table(client, dynamodb_table_name, True)

# If not in the dynamodb region - check if a replica exists, if not then create it
if aws_region.lower() != dynamodb_region:
    print(f"aws_region:{aws_region}, dynamodb_region:{dynamodb_region}")
    describe_table_response = region_client.describe_table(TableName=dynamodb_table_name)
    print(f"describe_table_response: {describe_table_response}")
    
    replica_already_created = False
    if "Replicas" in describe_table_response['Table']:
        for replica in describe_table_response['Table']['Replicas']:
            print(f"replica: {replica}")
            replica_region = replica['RegionName']
            if replica_region.lower() == aws_region.lower():
                replica_already_created = True
                break

    if not replica_already_created:
        print("Replica is not already created - creating")
        _create_dynamodb_table(region_client, dynamodb_table_name, True)
        create_global_table_response = client.create_global_table(
            GlobalTableName=dynamodb_table_name,
            ReplicationGroup=[
                {
                    'RegionName': aws_region
                },
            ]
        )
        print(f"create_global_table_response: {create_global_table_response}")


