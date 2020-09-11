import boto3

client = boto3.client('ec2')

class EBS(object):
    @classmethod
    def get_volumes(cls):
        volumes = []
        ebs = client.describe_volumes()
        for volume in ebs['Volumes']:
            temp_dict = {}
            volume_id = volume['VolumeId']
            volume_state = volume['State']
            volume_type = volume['VolumeType']
            temp_dict['volume_id'] = volume_id
            temp_dict['volume_state'] = volume_state
            temp_dict['volume_type'] = volume_type
            volumes.append(temp_dict)