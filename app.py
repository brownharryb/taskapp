import logging
from flask import Flask
from tasks.routes import task

app = Flask(__name__)

# Load Config
app.config.from_object('config')

# Init Logging
logging.basicConfig(format='%(asctime)-15s %(message)s', filename=app.config.get('LOG_FILENAME'))

# Register Blueprint
app.register_blueprint(task)

if __name__ == '__main__':
    app.run(host='0.0.0.0')