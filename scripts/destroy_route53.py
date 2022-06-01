import os
import boto3

aws_region = os.environ['CHOOSEN_AWS_REGION']
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
application_type = os.environ['APPLICATION_TYPE']

global_accelerator_region = "us-west-2"
base_route53_region = "us-east-1"
base_application_dns = "atu-dissertation.com."
global_Accelerator_hosted_zone_id = 'Z2BJ6XQ5FK7U4H'

print("In destroy route53")

client = boto3.client('globalaccelerator',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=global_accelerator_region)

route53_client = boto3.client('route53',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=base_route53_region)

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
        hosted_zones_response = route53_client.list_hosted_zones()
        print(f"hosted_zones_response: {hosted_zones_response}")
        hosted_zone_id = ''
        for hosted_zone in hosted_zones_response['HostedZones']:
            print(f"hosted_zone: {hosted_zone}")
            if hosted_zone['Name'].lower() == base_application_dns:
                hosted_zone_id = hosted_zone['Id']
                break

        print(f"hosted_zone_id 1:{hosted_zone_id}")
        hosted_zone_str = '/hostedzone/'
        hosted_zone_id = hosted_zone_id[len(hosted_zone_str):]
        print(f"hosted_zone_id 2:{hosted_zone_id}")
            
        global_accelerator_dns_name = accelerator_dns
        print(f"global_accelerator_dns_name:{global_accelerator_dns_name}")

        application_type_dns_name = f'{application_type}.atu-dissertation.com'
        print(f"application_type_dns_name:{application_type_dns_name}")

        list_resource_record_sets_response = route53_client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
        print(f"list_resource_record_sets_response:{list_resource_record_sets_response}")

        change_resource_record_sets_response = route53_client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': application_type_dns_name,
                        'Type': 'A',
                        'SetIdentifier': 'Simple',
                        'Region': 'us-east-1',
                        'AliasTarget': {
                            'HostedZoneId': global_Accelerator_hosted_zone_id,
                            'DNSName': global_accelerator_dns_name,
                            'EvaluateTargetHealth': True
                        }
                    }
                }, 
            ]
        }
    )
        print(f"change_resource_record_sets_response: {change_resource_record_sets_response}")
        break


