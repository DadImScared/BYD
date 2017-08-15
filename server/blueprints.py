from resources.users import user_api


def register_blueprints(app):
    """Register blueprints to flask app"""
    app.register_blueprint(user_api)
