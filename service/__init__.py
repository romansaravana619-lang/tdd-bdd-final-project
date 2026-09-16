from flask import Flask
from service import config

app = Flask(__name__, static_folder="static")
app.config.from_object(config)

from service import routes  # noqa: E402,F401
from service.models import init_db  # noqa: E402

init_db(app)
