import sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS DADOS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            """
        )

        quantidade = conn.execute("SELECT COUNT(*) FROM dados").fetchone()[0]

        if quantidade == 0:
            dados_padrao = [("admin", "admin")]

            for username, password in dados_padrao:
                conn.execute("INSERT INTO dados (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
init_db()

@app.route("/cadastro", methods=["POST"])
def cadastrar():
    dados = request.get_json()
    username = dados.get("username")
    password = dados.get("password")

    if not username or not password:
        return jsonify({"erro":"Todos os campos são obrigatórios"}),400
    
    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO dados (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        return jsonify({"mensagem":"Cadastro feito com sucesso"}),201
    except sqlite3.IntegrityError:
        return jsonify ({"erro":"Usuário já cadastrado"}),400
    except Exception as e:
        return jsonify({"erro":f"Erro inesperado ao cadastrar usuário {str(e)}"}),500


if __name__ == "__main__":
    app.run(debug=True)