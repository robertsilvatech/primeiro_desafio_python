from telegram import Bot
from telegram import BotCommand

token = '1288974768:AAGslAaJ-OY0B6UZQgwrB8CHnhF-2t1T_aw'
bot = Bot(token=token)


def main():
    commands = [
        BotCommand("aws_ec2_all", "List all ec2 instances"),
        BotCommand("aws_ec2_start_instance", "Start ec2 instance (e.g /aws_ec2_start_instance <instance_id>"),
        BotCommand("aws_ec2_stop_instance", "Stop ec2 instance (e.g /aws_ec2_stop_instance <instance_id>")
        BotCommand("aws_ec2_stop_instance", "Stop ec2 instance (e.g /aws_ec2_stop_instance <instance_id>")
    ]

    set_commands = bot.set_my_commands(commands=commands)
    return set_commands
