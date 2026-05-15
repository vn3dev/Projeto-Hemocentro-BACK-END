from flask import Flask
from routes.doadores import doadores_bp
from routes.bolsas import bolsas_bp
from routes.sangue import sangue_bp
from flask_cors import CORS

app = Flask(__name__)
CORS = CORS(app)  # Habilita CORS para toda a aplicação

# mantem a ordem dos atributos na hora de exibir o json pq sou fresco
app.json.sort_keys = False

# registra os blueprints
app.register_blueprint(doadores_bp)
app.register_blueprint(bolsas_bp)
app.register_blueprint(sangue_bp)

app.run(debug = True)