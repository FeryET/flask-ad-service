def test_app(app):
    assert app.config["TESTING"] is True
