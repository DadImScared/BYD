from server.app import create_app
from server.settings import ProdConfig
import config


if config.DEBUG:
    app = create_app()
else:
    app = create_app(ProdConfig)

if __name__ == '__main__':
    app.run()
