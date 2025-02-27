from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from application.controllers.talk.TalkController import TalkController


load_dotenv('./config/.env')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.add_url_rule('/talk=<rag>', 'talk', TalkController.talk, methods=['POST'])


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)


