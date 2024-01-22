import os

from khl import Bot, Cert

if os.path.exists('config_private.py'):
    import config_private as config
else:
    import config


bot = Bot(cert = Cert(token=config.token,
                      verify_token=config.verify_token,
                      encrypt_key=config.encrypt_key),
          port=config.webhook_port,
          route=config.webhook_route
)
