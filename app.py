from flask import Flask
from routes.main_routes import main_bp
from routes.search_routes import search_bp
#from routes.admin_routes import admin_bp

app = Flask(__name__)
app.register_blueprint(main_bp)
app.register_blueprint(search_bp)
#app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
