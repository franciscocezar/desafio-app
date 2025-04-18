from services.data_manager import DataManager
from database.conexao import Database
from flask import Flask, jsonify


data = DataManager()

app = Flask(__name__)
        
@app.route('/acoes', methods=['GET'])
def get_all():
    conn = Database()
    conn.conecta_bd()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
    
    try:
        retorno = conn.get_all()
        return jsonify(retorno)
    except Error as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.desconecta_bd()
            

@app.route('/acoes/<string:ticker>', methods=['GET'])
def get_acao(ticker):
    conn = Database()
    conn.conecta_bd()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
    
    try:
        retorno = conn.get_acao(ticker)
        return jsonify(retorno)
    except Error as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.desconecta_bd()

if __name__ == '__main__':
    app.run()