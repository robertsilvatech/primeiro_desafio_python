import boto3

ec2_client = boto3.client('ec2', region_name='us-east-1')

def ec2_all():
    ec2_list = []
    response = ec2_client.describe_instances()
    if isinstance(response, dict):
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                temp_dict = {}
                instance_type = instance['InstanceType']
                instance_state = instance['State']
                instance_state_code = instance_state['Code']
                instance_state_name = instance_state['Name']
                instance_id = instance['InstanceId']
                instance_name = instance['Tags'][0]['Value']
                temp_dict['instance_type'] = instance_type
                temp_dict['instance_state'] = instance_state
                temp_dict['instance_state_code'] = instance_state_code
                temp_dict['instance_state_name'] = instance_state_name
                temp_dict['instance_id'] = instance_id
                temp_dict['instance_name'] = instance_name
                ec2_list.append(temp_dict)
                print(f'{instance_id} - {instance_type} - {instance_state_code} - {instance_state_name}')
    return ec2_list

def ec2_start(instance_id):
    response = ec2_client.start_instances(InstanceIds=[instance_id])
    current_state = response['StartingInstances'][0]['CurrentState']['Name']
    previous_state = response['StartingInstances'][0]['PreviousState']['Name']
    message = f'Instance Id {instance_id} current state is {current_state} and previous state was {previous_state}'
    return message

def ec2_stop(instance_id):
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    current_state = response['StoppingInstances'][0]['CurrentState']['Name']
    previous_state = response['StoppingInstances'][0]['PreviousState']['Name']
    message = f'Instance Id {instance_id} current state is {current_state} and previous state was {previous_state}'
    return message

