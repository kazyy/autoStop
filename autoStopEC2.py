import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:autoStop',
                'Values':[
                    'true',
                ]
            }
        ],
        MaxResults=5
    )
    if len(response['Reservations']) == 0:
        print("no target for autoStop")
    else:
        for instance in response['Reservations'][0]['Instances']:
            if instance['State']['Name'] == 'running':
                print('stopping: ' + instance['InstanceId'])
                ec2.stop_instances(InstanceIds=[instance['InstanceId']])
                print('stopped: ' + instance['InstanceId'])
            else:
                print('no operation for autoStop: ' + instance['InstanceId'])
