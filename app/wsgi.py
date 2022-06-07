from app import application


def start():
    application.app.run(host='0.0.0.0', port=8000, use_reloader=False)


if __name__ == "__main__":
    start()
