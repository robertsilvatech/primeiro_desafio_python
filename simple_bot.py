import os
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from handlers.aws.ec2 import ec2_all
from handlers.aws.ec2 import ec2_start
from handlers.aws.ec2 import ec2_stop
from handlers.aws.iam import iam_users
from handlers.aws.iam import iam_check_user_mfa_device
from handlers.aws.iam import iam_users_without_mfa_devices
from handlers.vmware.vcenter import login_vmware
from handlers.vmware.vcenter import logout_vmware
from handlers.vmware.vcenter import list_vms
from handlers.vmware.vcenter import poweron_vm
from handlers.vmware.vcenter import poweroff_vm
from handlers.vmware.vcenter import update_cpu
from handlers.vmware.vcenter import get_datastores
from handlers.vmware.vcenter import get_cluster_id
from handlers.vmware.vcenter import get_datastore_id
from handlers.vmware.vcenter import get_folder_id
from handlers.vmware.vcenter import create_vm_default
from handlers.vmware.vcenter import delete_vm
from configure_bot import main as config_bot
from security.mfa import key_mfa


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
    instances = ec2_all()
    message = ''
    for instance in instances:
        instance_id = instance['instance_id']
        instance_name = instance['instance_name']
        instance_state_name = instance['instance_state_name']
        message += f'--> Instance Id: {instance_id} - Instance Name: {instance_name} - Instance State:{instance_state_name}\n'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def aws_ec2_start_instanceec(update, context):
    try:
        instance_id = context.args[0]
        action = ec2_start(instance_id)
        message = action
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    except:
        message = 'instance id is missing'
        context.bot.send_message(chat_id=update.message.chat_id, text=message)  

def aws_ec2_stop_instance(update, context):
    try:
        instance_id = context.args[0]
        action = ec2_stop(instance_id)
        message = action
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    except:
        message = 'instance id is missing'
        context.bot.send_message(chat_id=update.message.chat_id, text=message) 

def vcenter_list_vms(update, context):
    token_vmware = login_vmware()
    vms = list_vms(token=token_vmware)
    if vms:
        message = ''
        for vm in vms:
            vm_id = vm['vm_id']
            vm_name = vm['vm_name']
            vm_power_state = vm['vm_power_state']
            vm_cpu_count = vm['vm_cpu_count']
            vm_memory_size_mb = vm ['vm_memory_size_mb']
            message += f'--> ID: {vm_id} - Name: {vm_name} - State: {vm_power_state} - CPU: {vm_cpu_count} - Memory: {vm_memory_size_mb}\n'
            print(message)
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    logout_vmware(token)

def vcenter_poweroff_vm(update, context):
    token_vmware = login_vmware()
    vmname = context.args[0]
    message = poweroff_vm(token_vmware, vmname)
    print(message)
    context.bot.send_message(chat_id=update.message.chat_id, text=message)
    logout_vmware(token)

def vcenter_poweron_vm(update, context):
    token_vmware = login_vmware()
    try:
        vmname = context.args[0]
        message = poweron_vm(token_vmware, vmname)
    except:
        message = 'vm id is missing'
    
    context.bot.send_message(chat_id=update.message.chat_id, text=message)
    logout_vmware(token)

def vcenter_update_cpu(update, context):
    token_vmware = login_vmware()
    try:
        vmname = context.args[0]
        cpu = context.args[1]
        message = update_cpu(token_vmware, vmname, cpu)
        context.bot.send_message(chat_id=update.message.chat_id, text=message)    
    except:
        message = 'vm id or cpu count is missing'
        context.bot.send_message(chat_id=update.message.chat_id, text=message)    
    logout_vmware(token)

def vcenter_get_datastores(update, context):
    token_vmware = login_vmware()
    datastores = get_datastores(token_vmware)
    message = ''
    for datastore in datastores:
        datastore_name = datastore['datastore_name']
        datastore_type = datastore['datastore_type']
        datastore_utilization_perc = datastore['datastore_utilization_perc']
        message += f'--> Name: {datastore_name} - Type: {datastore_type} - Utilization in perc: {datastore_utilization_perc:.2f}%\n'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)    

def vcenter_create_vm_default(update, context):
    token_vmware = login_vmware()
    try:
        vmname = context.args[0]
        cluster_id = get_cluster_id(token_vmware)
        print(f'Cluster ID: {cluster_id}')
        datastore_name = 'Datastore_sf10hv08_01'
        datastore_id = get_datastore_id(token_vmware, datastore_name)
        print(f'Datastore ID: {datastore_id}')
        folder_id = get_folder_id(token_vmware)
        print(f'Folder ID: {folder_id}')
        message = create_vm_default(token_vmware, vmname ,cluster_id, datastore_id, folder_id) 
        context.bot.send_message(chat_id=update.message.chat_id, text=message)    
    except Exception as err:
        message = 'vmname is missing'
        context.bot.send_message(chat_id=update.message.chat_id, text=err)    

def vcenter_delete_vm(update, context):
    token_vmware = login_vmware()
    try:
        vmid = context.args[0]
        result = delete_vm(token_vmware, vmid)
        context.bot.send_message(chat_id=update.message.chat_id, text=result)    
    except:
        message = 'vm id is missing'
        context.bot.send_message(chat_id=update.message.chat_id, text=message)    

token = os.getenv('TOKEN_TG')

def main():
    conf = config_bot()
    print(conf)
    print('Aqui')
    updater = Updater(token=token, use_context=True)
    # Dispatcher: Envia as mensagens para os handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('aws_ec2_all', aws_ec2_all))
    dispatcher.add_handler(CommandHandler('aws_ec2_start_instance', aws_ec2_start_instance))
    dispatcher.add_handler(CommandHandler('aws_ec2_stop_instance', aws_ec2_stop_instance))
    dispatcher.add_handler(CommandHandler('vcenter_list_vms', vcenter_list_vms))
    dispatcher.add_handler(CommandHandler('vcenter_poweron_vm', vcenter_poweron_vm))
    dispatcher.add_handler(CommandHandler('vcenter_poweroff_vm', vcenter_poweroff_vm))
    dispatcher.add_handler(CommandHandler('vcenter_update_cpu', vcenter_update_cpu))
    dispatcher.add_handler(CommandHandler('vcenter_get_datastores', vcenter_get_datastores))
    dispatcher.add_handler(CommandHandler('vcenter_create_vm_default', vcenter_create_vm_default))
    dispatcher.add_handler(CommandHandler('vcenter_delete_vm', vcenter_delete_vm))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    # Start the Bot
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()