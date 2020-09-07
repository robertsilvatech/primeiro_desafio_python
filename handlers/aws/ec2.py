import boto3

ec2_client = boto3.client('ec2', region_name='us-east-1')
response = ec2_client.describe_instances()

class AWSEC2(object):
    @classmethod
    def ec2_all(cls):
        ec2_list = []
        if isinstance(response, dict):
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    temp_dict = {}
                    instance_type = instance['InstanceType']
                    instance_state = instance['State']
                    instance_state_code = instance_state['Code']
                    instance_state_name = instance_state['Name']
                    instance_id = instance['InstanceId']
                    temp_dict['instance_type'] = instance_type
                    temp_dict['instance_state'] = instance_state
                    temp_dict['instance_state_code'] = instance_state_code
                    temp_dict['instance_state_name'] = instance_state_name
                    temp_dict['instance_id'] = instance_id
                    ec2_list.append(temp_dict)
                    print(f'{instance_id} - {instance_type} - {instance_state_code} - {instance_state_name}')
        return ec2_list

    @classmethod
    def ec2_start(cls, instance_id):
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        return response

    @classmethod
    def ec2_stop(cls, instance_id):
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        return response

    @classmethod
    def ec2_state(cls, instance_id):
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']
        return state
