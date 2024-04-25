from src.app import create_app
if __name__ == '__main__':
    app = create_app()
    create_app().run(debug=True, port=7890)