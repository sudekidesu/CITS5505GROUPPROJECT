from flask_migrate import Migrate

from app.config import DeploymentConfig
from app import create_app, db
app = create_app(DeploymentConfig)
migrate = Migrate(app, db)

