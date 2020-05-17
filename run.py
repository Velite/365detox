from configuration import TestConfig
from main import create_app

app = create_app(TestConfig)
if __name__ == "__main__":
	app.run(debug = app.debug)
