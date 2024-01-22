import os
import json
import logging
import subprocess

from khl import Bot, Cert, Message

# config validation
if os.path.exists('config_private.json'):
    with open('config_private.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    required_keys = ['token', 'verify_token', 'encrypt_key', 'client_id', 'client_secret', 'webhook_port', 'webhook_route']
    for key in required_keys:
        if key not in config:
            logging.log(logging.ERROR, f'config_private.json missing key: {key}')
            exit(1)
else:
    logging.log(logging.ERROR, 'config_private.json not found')
    exit(1)


# init bot
# logging.log(logging.INFO, 'NaziBot is starting...')
bot = Bot(cert = Cert(token=config['token'],
                      verify_token=config['verify_token'],
                      encrypt_key=config['encrypt_key']),
          port=config['webhook_port'],
          route=config['webhook_route']
)

def run_sh(path: str):
    if os.path.exists(path):
        result = subprocess.run(path, shell=True, stdout=subprocess.PIPE, text=True)
        return result.stdout
    else:
        return f'{path} not found.'


@bot.command()
async def help(msg: Message):
    result = """
    /start  启动服务器
    /stop   关闭服务器
    """
    await msg.reply(result)

@bot.command()
async def test(msg: Message):
    await msg.reply("我是纳兹熊")

@bot.command()
async def start(msg: Message):
    """start server.
    
    """
    command = '/home/admin/start_server.sh'
    result = run_sh(command)
    await msg.reply(f'{result}')

@bot.command()
async def stop(msg: Message):
    """stop server.
    """
    command = '/home/admin/stop_server.sh'
    result = run_sh(command)
    await msg.reply(f'{result}')

if __name__ == '__main__':
    print('Nazibot is starting...')
    print(config)
    bot.run()