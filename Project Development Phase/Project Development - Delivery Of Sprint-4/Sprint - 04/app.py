from registry import create_app

if __name__ == "__main__":
    app = create_app().run(debug=True)
