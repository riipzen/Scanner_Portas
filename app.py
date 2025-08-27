from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def Conectar_BD():
    conn = sqlite3.connect('meu_banco.db')
    return conn


@app.route('/criar_tabela', methods=['GET'])
def criar_tabela():
    conn = sqlite3.connect('meu_banco.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios(id INTEGER  PRIMARY KEY AUTOINCREMENT, nome VARCHAR(200) NOT NULL, email VARCHAR(200) NOT NULL UNIQUE )")
    conn.commit()
    conn.close()
    return jsonify({"Mensagem": "Tabela Usuarios criada com sucesso"}), 201

@app.route('/usuarios', methods=['POST'])
def adicionar_usuario():
    novos_usuarios = request.get_json()
    nome = novos_usuarios['nome']
    email = novos_usuarios['email']

    try:
        conn = sqlite3.connect('meu_banco.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios(nome, email) VALUES (?, ?)", (nome, email))
        conn.commit()
        return jsonify({"Mensagem", "Usuario adicionado com sucesso"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"Mensagem": "Esse email ja existe!"}), 400
    finally:
        conn.close()


@app.route("/usuarios", methods=['GET'])
def listar_usuario():
    conn = sqlite3.connect('meu_banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios")
    usuarios_db = cursor.fetchall()
    conn.close()

    usuario_json = []
    for usuario in usuarios_db:
       usuario_json.append({
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2]
    })
 
    return jsonify(usuario_json), 200

if __name__ == '__main__':
    app.run(debug=True)
