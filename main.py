from app.run_app import app
from config.config import debug

if __name__ == '__main__':
    app.run(debug=debug, use_reloader=False)






