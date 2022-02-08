import boto3

session = boto3.Session(region_name = 'eu-west-2')
credentials = session.get_credentials()
if not credentials:
    raise Exception('The credentials appear to be empty')
ec2_client = boto3.client('ec2')
response = ec2_client.describe_instances().get('Reservations')
unencryptedInstances = []
count = 0
for Reservation in response:
    for instance in Reservation['Instances']:
        for device in instance['BlockDeviceMappings']:
            if device['DeviceName'] == instance['RootDeviceName']:
                volID = device['Ebs']['VolumeId']
                encryptionStatus = ec2_client.describe_volumes(
                    VolumeIds=[
                        volID,
                    ]
                )['Volumes'][0]['Encrypted']
                for tags in instance['Tags']:
                    if tags['Key'] == 'Name':
                        InstanceName = tags['Value']
                if encryptionStatus == False:
                    unencryptedInstances.append([InstanceName, volID])
                    print(count)
                    count += 1
for line in unencryptedInstances:
    print(line)

