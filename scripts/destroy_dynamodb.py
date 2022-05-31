import os
import boto3
import time 
aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']

dynamodb_region = "us-east-1"
dynamodb_table_name = "users"

print("In Destroy DynamoDB")

client = boto3.client('dynamodb',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=dynamodb_region)

region_client = boto3.client('dynamodb',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=aws_region)


def _delete_table(boto3_client, table_name):
    list_tables_response = boto3_client.list_tables()
    print(f"list_tables_response: {list_tables_response}")

    for table_name in list_tables_response['TableNames']:
        print(f"table_name: {table_name}")

        if table_name.lower() == dynamodb_table_name.lower():
            table_status = "empty"
            count = 0
            while table_status.lower() != "active" and table_status != "deleted":
                if count > 0:
                    sleep_time = 5 + count
                    print(f" Sleeping for {sleep_time} seconds")
                    time.sleep(sleep_time)
                try:
                    describe_table_response = boto3_client.describe_table(TableName=table_name)
                    print(f"describe_table_response: {describe_table_response}")
                    table_status = describe_table_response['Table']['TableStatus']
                    print(f"table_status: {table_status}")
                except:
                    print("Unable to find table")
                    table_status = "deleted"
                count += 1

            try:
                delete_table_response = boto3_client.delete_table(TableName=table_name)
                print(f"delete_table_response: {delete_table_response}")
            except:
                print("Unable to delete table")

_delete_table(client, dynamodb_table_name)
_delete_table(region_client, dynamodb_table_name)
    

