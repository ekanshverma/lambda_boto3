import boto3
ec2 = boto3.resource('ec2')
rds = boto3.client('rds')

def lambda_handler(event, context):
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    instances = ec2.instances.filter(Filters=filters)
    RunningInstances = []
    for instance in instances:
        RunningInstances.append(instance.id)
        print(instance.id)
    ec2.create_tags(
    Resources=RunningInstances,
    Tags=[
        {
            'Key': 'env',
            'Value': 'dev'
        }
        ]
    )
    dbs = rds.describe_db_instances()
    db_arn=[]
    db_running_arn=[]
    for i in range(len(dbs['DBInstances'])):
        db_arn.append(dbs['DBInstances'][i]['DBInstanceArn'])
    for i in db_arn:
        dbs = rds.describe_db_instances(Filters=[
            {
                'Name': 'db-instance-id', 
                'Values': [i]
            }
            ])
        if dbs['DBInstances'][0]['DBInstanceStatus'] == 'available':
            db_running_arn.append(i)
            response_tags = rds.add_tags_to_resource(
            ResourceName=i,
            Tags=[
                {
                    'Key': 'Project',
                    'Value': 'project_name'
                },
                ]
            )
    print(db_running_arn)

