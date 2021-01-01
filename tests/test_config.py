def test_testing_config(test_app):
    config = test_app.application.config

    assert config["DB_NAME"] == "notaveltest"
    assert config["TESTING"]
    assert config["DEBUG"]
    assert "notaveltest" in config["SQLALCHEMY_DATABASE_URI"]
