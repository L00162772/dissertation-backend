import os
import boto3

aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']

dynamodb_region = "us-east-1"
dynamodb_table_name = "users"

print("In setup DynamoDB")

client = boto3.client('dynamodb',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=dynamodb_region)

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
    create_table_response = client.create_table(TableName=table_name)
    print(f"create_table_response: {create_table_response}")

# If not in the dynamodb region - check if a replica exists, if not then create it
if aws_region.lower() == dynamodb_region:
    describe_table_response = client.describe_table(TableName=table_name)
    print(f"describe_table_response: {describe_table_response}")
    
    replica_already_created = False
    for replica in describe_table_response['Table']['Replicas']:
        print(f"replica: {replica}")
        replica_region = replica['RegionName']
        if replica_region.lower() == aws_region.lower():
            replica_already_created = True
            break

    if not replica_already_created:
        print("Replica is not already created - creating")
        create_global_table_response = client.create_global_table(
            GlobalTableName=dynamodb_table_name,
            ReplicationGroup=[
                {
                    'RegionName': aws_region
                },
            ]
        )
        print(f"create_global_table_response: {create_global_table_response}")

