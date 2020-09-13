from telegram import Bot
from telegram import BotCommand

token = '1288974768:AAGslAaJ-OY0B6UZQgwrB8CHnhF-2t1T_aw'
bot = Bot(token=token)

def main():
    commands = [
        BotCommand("start","Start Bot"),
        BotCommand("aws_ec2_all","List all ec2 instances"),
        BotCommand("aws_ec2_start_instance", "Start ec2 instance"),
        BotCommand("aws_ec2_stop_instance", "Stop ec2 instance"),
        BotCommand("vcenter_list_vms", "List VMS on vCenter"),
        BotCommand("vcenter_poweron_vm", "PowerON VM"),
        BotCommand("vcenter_poweroff_vm", "PowerOFF VM"),
        BotCommand("vcenter_update_cpu", "Update CPU Core from VM"),
        BotCommand("vcenter_get_datastores", "Get utilization from datastores"),
        BotCommand("vcenter_create_vm_default", "Create a new with defaults"),
        BotCommand("vcenter_delete_vm", "Delete a VM"),
        ]
    set_commands = bot.set_my_commands(commands=commands)
    return set_commands
