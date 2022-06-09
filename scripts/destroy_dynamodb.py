import os
import boto3
import time 

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


def _delete_main_table(boto3_client, table_name):
    _wait_until_replicas_deleted(boto3_client, dynamodb_table_name)
    _wait_until_table_ready(boto3_client, dynamodb_table_name)

    list_tables_response = boto3_client.list_tables()
    print(f"list_tables_response: {list_tables_response}")

    table_found = False
    for table_name in list_tables_response['TableNames']:
        print(f"table_name: {table_name}")

        if table_name.lower() == dynamodb_table_name.lower():
            table_status = "empty"
            count = 0
            while table_status.lower() != "active" and table_status != "deleted":
                if count > 0:
                    sleep_time = 5 + count
                    print(f"_delete_main_table Sleeping for {sleep_time} seconds")
                    time.sleep(sleep_time)
                try:
                    describe_table_response = boto3_client.describe_table(TableName=table_name)
                    print(f"describe_table_response: {describe_table_response}")
                    table_status = describe_table_response['Table']['TableStatus']
                    print(f"table_status: {table_status}")
                    table_found = True
                except:
                    print("(_delete_table)Unable to find table")
                    table_status = "deleted"
                    table_found = False
                count += 1

            if table_found:
                try:
                    delete_table_response = boto3_client.delete_table(TableName=table_name)
                    print(f"delete_table_response: {delete_table_response}")
                except Exception as e:
                    print(f"Unable to delete table. Exception:{e}")
            

def _wait_until_table_ready(boto3_client, table_name):         
    table_status = "empty"
    count = 0
    while table_status.lower() != "active" and table_status.lower() != "deleted" and count < 10:
        if count > 0:
            sleep_time = 5 + count
            print(f"_wait_until_table_ready Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
        
        count += 1
        try:
            describe_table_response = boto3_client.describe_table(TableName=table_name)
            print(f"describe_table_response: {describe_table_response}")
            table_status = describe_table_response['Table']['TableStatus']
            print(f"table_status: {table_status}")
        except:
            print("(_wait_until_table_ready)Unable to find table")
            table_status = "deleted"

def _wait_until_replicas_deleted(boto3_client, table_name):
    count = 0
    replica_count = 999
    while replica_count > 0 and count < 100:
        if count > 0:
            sleep_time = 5 + count
            print(f"_wait_until_replicas_deleted Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
        
        count += 1
        try:
            describe_table_response = boto3_client.describe_table(TableName=table_name)
            print(f"describe_table_response: {describe_table_response}")
            replicas = describe_table_response['Table']['Replicas']
            print(f"replicas: {replicas}")
            replica_count = len(replicas)
            print(f"replica_count: {replica_count}")
        except:
            print("(_wait_until_replicas_deleted)Unable to find table")
            replica_count = 0 

def _delete_replica_table(boto3_client, region):
    print(f"Delete replica in region: {region}")
    _wait_until_table_ready(client, dynamodb_table_name)
  
    delete_replica_response = boto3_client.update_table(
                TableName=dynamodb_table_name,
                ReplicaUpdates = 
                [
                    {
                    "Delete": {
                        "RegionName": region
                    }
                    }
                ]
    )
    print(f"delete_replica_response: {delete_replica_response}")

def _destroy_replicas(boto3_client):
    try:
        describe_table_response = boto3_client.describe_table(TableName=dynamodb_table_name)
        print(f"describe_table_response: {describe_table_response}")
        for replica in describe_table_response['Table']['Replicas']:
            print(f"replica: {replica}")
            _delete_replica_table(boto3_client, replica['RegionName'])
        table_status = describe_table_response['Table']['TableStatus']
        print(f"table_status: {table_status}")
    except Exception as e:
        print(f"Unable to find table {dynamodb_table_name}. Exception: {e}")


_destroy_replicas(client)
_delete_main_table(client, dynamodb_table_name)
    

