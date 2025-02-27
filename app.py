from flask import Flask
from dotenv import load_dotenv
from application.controllers.talk.TalkController import TalkController

load_dotenv('./config/.env')

app = Flask(__name__)

app.add_url_rule('/talk=<rag>', 'talk', TalkController.talk, methods=['POST'])

app.run(debug=True, host='0.0.0.0', port=3000)


