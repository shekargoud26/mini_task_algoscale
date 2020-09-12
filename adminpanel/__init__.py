import os

from flask import Flask

from adminpanel import db, auth, admin

# defining the application factory
def create_app(test_config=None):
    # creating and configuring the app
    app = Flask(__name__, instance_relative_config=True)
    # basic configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'adminpanel.sqlite')
    )
    # ensuring instance folder exists
    # this is where the sqlite db will be stored
    try:
        os.makedirs(app.instance_path)  
    except OSError:
        pass

    db.init_app(app)
    # registering blueprints for auth module
    app.register_blueprint(auth.bp)
    # registering blueprints for admin module
    app.register_blueprint(admin.bp)

    app.add_url_rule('/', endpoint='index')


    return app