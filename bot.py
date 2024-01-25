import os
import json
import logging
import subprocess

from khl import Bot, Cert, Message
from rcon.source import Client

# config validation
if os.path.exists('config_private.json'):
    with open('config_private.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    required_keys = ['token', 'verify_token', 'encrypt_key', 'client_id', 'client_secret', 'access_key', 
                     'secret_key', 'server_id', 'project_id', 'webhook_port', 'webhook_route', 'server_ip',
                     'rcon_port', 'admin_password']
    for key in required_keys:
        if key not in config:
            logging.log(logging.ERROR, f'config_private.json missing key: {key}')
            exit(1)
else:
    logging.log(logging.ERROR, 'config_private.json not found')
    exit(1)

# extract
token = config['token']
verify_token = config['verify_token']
encrypt_key = config['encrypt_key']
client_id = config['client_id']
client_secret = config['client_secret']
access_key = config['access_key']
secret_key = config['secret_key']
server_id = config['server_id']
project_id = config['project_id']
webhook_port = config['webhook_port']
webhook_route = config['webhook_route']
server_ip = config['server_ip']
rcon_port = config['rcon_port']
admin_password = config['admin_password']

# init bot
# logging.log(logging.INFO, 'NaziBot is starting...')
bot = Bot(cert = Cert(token=token, verify_token=verify_token, encrypt_key=encrypt_key),
          port=webhook_port,
          route=webhook_route
)

# init rcon client
rcon_client = Client(server_ip, rcon_port, passwd=admin_password)

def run_sh(path: str):
    if os.path.exists(path):
        result = subprocess.run(path, shell=True, stdout=subprocess.PIPE, text=True)
        return result.stdout
    else:
        return f'{path} not found.'

def is_any_player():
    command = 'ShowPlayers'
    result = rcon_client.run(command)
    print(result)
    if result == 'No Players Connected':
        return False
    else:
        return True

@bot.command()
async def help(msg: Message):
    result = """
    /help   查看帮助
    /start  启动服务器
    /stop   关闭服务器
    /test   测试信息
    """
    await msg.reply(result)

@bot.command()
async def test(msg: Message):
    result = rcon_client.run('ShowPlayers')
    await msg.reply(result)

@bot.command()
async def start(msg: Message):
    """start server.
    """
    # command = '/home/admin/start_server.sh'
    # result = run_sh(command)
    result = '华为云API有问题，现在只能手动开启ECS服务器'
    await msg.reply(f'{result}')

@bot.command()
async def stop(msg: Message):
    """stop server.
    """
    # command = '/home/admin/stop_server.sh'
    # result = run_sh(command)
    if is_any_player():
        result = '服务器有玩家在线，不允许关闭服务器。'
    else:
        try:
            rcon_client.run('Shutdown 60 "Server will be stopped in 60s."')
            await msg.reply('服务器将于60s后关闭。')
            result = '华为云API有问题，现在只能手动关闭ECS服务器。'
        except:
            result = '服务器关闭失败。请检查服务器日志。'
    await msg.reply(f'{result}')

@bot.command
async def status(msg: Message):
    """show server status.
    """
    command = 'ShowPlayers'
    result = rcon_client.run(command)
    await msg.reply(f'现在服务器中有{result}人。')

if __name__ == '__main__':
    print('Nazibot is starting...')
    print(config)
    bot.run()