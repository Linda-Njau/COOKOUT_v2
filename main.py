from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.test_request_context():
        print("Routes")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}:{rule}")
    app.run(debug=True)
