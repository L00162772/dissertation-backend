import os
import boto3

aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

print("aws_region:", aws_region)
print("aws_access_key_id:", aws_access_key_id)
print("aws_secret_access_key:", aws_secret_access_key)
print("In invalidate_cloudfront_distribution")

client = boto3.client('cloudfront', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
print("Here 2")  
list_distributions_response = client.list_distributions()
print(f"list_distributions_response: {list_distributions_response}")

distribution_id = ''
for item in list_distributions_response['DistributionList']['Items']:
    print(f" item: {item}")
    print(f" DistributionId: {item['Id']}")
    distribution_id = item['Id']
    print(f" DistributionId: {item['ARN']}")
    tags_for_resource_response = client.list_tags_for_resource(Resource=item['ARN'])
    print(f"tags_for_resource_response: {tags_for_resource_response}")
    has_backend_tag = False
    has_region_tag = False
    for tag in tags_for_resource_response['Tags']['Items']:
        print(f" tag: {tag}")
        key = tag['Key']
        value = tag['Value']
        if key == 'Name' and value.lower() == 'backend':
            has_backend_tag = True
        if key == 'Region' and value.lower() == aws_region.lower():
            has_region_tag = True
        
        print(f" has_backend_tag: {has_backend_tag}")
        print(f" has_region_tag: {has_region_tag}")
    
    if has_backend_tag and has_region_tag:
        break;


create_invalidation_response = client.create_invalidation(
    DistributionId=distribution_id,
    InvalidationBatch={
        'Paths': {
            'Quantity': 1,
            'Items': ['/*']
        },
        'CallerReference': 'githubActions'
    }
)
print(f"create_invalidation_response: {create_invalidation_response}")
