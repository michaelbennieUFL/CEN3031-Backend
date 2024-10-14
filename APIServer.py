from app import create_app
from Extensions import DATABASE as db

if __name__ == '__main__':
    api_server =create_app()

    with api_server.app_context():
        db.create_all()
    api_server.run(host='0.0.0.0', port=5002)