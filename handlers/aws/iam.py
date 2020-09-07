import boto3

client = boto3.client('iam')

class IAM(object):
    @classmethod
    def iam_users(cls):
        users = []
        get_users = client.list_users()
        if get_users:
            for user in get_users['Users']:
                user_name = user['UserName']
                users.append(user_name)
        return users

    @classmethod
    def iam_check_user_mfa_device(cls, username):
        get = client.list_mfa_devices(UserName=username)
        mfa_devices = get['MFADevices']
        return mfa_devices

    @classmethod
    def iam_users_without_mfa_devices(cls):
        users_without = []
        for user in cls.iam_users():
            state = cls.iam_check_user_mfa_device(username=user)
            if not state:
                users_without.append(user)
        return users_without