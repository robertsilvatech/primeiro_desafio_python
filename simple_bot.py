import inspect
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from handlers.aws.ec2 import AWSEC2
from handlers.aws.iam import IAM
from handlers.aws.ebs import EBS
from configure_bot import main as config_bot


def start(update, context):
    message = 'Seja bem vindo ao desafio Python'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def echo(update, context):
    message = 'echo'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def unknown(update, context):
    message = 'unknown'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def aws_ec2_all(update, context):
    instances = AWSEC2.ec2_all()
    message = ''
    for instance in instances:
        instance_id = instance['instance_id']
        instance_state_name = instance['instance_state_name']
        #info = f'{instance_id} - {instance_state_name}\n'
        message += instance_id + '\n'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def aws_ec2_start_instance(update, context):
    instance_id = context.args[0]
    instances = AWSEC2.ec2_start(instance_id)
    message = instances
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def aws_ec2_stop_instance(update, context):
    instance_id = context.args[0]
    instances = AWSEC2.ec2_stop(instance_id)
    message = instances
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def aws_ec2_state_instance(update, context):
    instance_id = context.args[0]
    instances = AWSEC2.ec2_state(instance_id)
    message = instances
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def aws_iam_get_users(update, context):
    users = IAM.iam_users()
    message = ''
    for user in users:
        message += user + '\n'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def aws_iam_users_without_mfa_devices(update, context):
    users = IAM.iam_users_without_mfa_devices()
    message = ''
    for user in users:
        message += user + '\n'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def aws_ebs_get_all(update, context):
    volumes = EBS.get_volumes()
    message = ''
    for volume in volumes:
        volume_id = volume['volume_id']
        volume_type = volume['volume_type']
        volume_state = volume['volume_state']
        message += f'VolumeId: {volume_id} - Volume Type: {volume_type} - Volume State: {volume_state}\n'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

token = '1288974768:AAGslAaJ-OY0B6UZQgwrB8CHnhF-2t1T_aw'


def main():
    conf = config_bot()
    print(conf)
    updater = Updater(token=token, use_context=True)
    # Dispatcher: Envia as mensagens para os handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('aws_ec2_all', aws_ec2_all))
    dispatcher.add_handler(CommandHandler('aws_ec2_start_instance', aws_ec2_start_instance))
    dispatcher.add_handler(CommandHandler('aws_ec2_stop_instance', aws_ec2_stop_instance))
    dispatcher.add_handler(CommandHandler('aws_ec2_state_instance', aws_ec2_state_instance))
    dispatcher.add_handler(CommandHandler('aws_iam_get_users', aws_iam_get_users))
    dispatcher.add_handler(CommandHandler('aws_iam_users_without_mfa', aws_iam_users_without_mfa_devices))
    dispatcher.add_handler(CommandHandler('aws_ebs_get_all', aws_ebs_get_all))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    # Start the Bot
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()