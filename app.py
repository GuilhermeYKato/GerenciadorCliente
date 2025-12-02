from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder="src")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
BD_PORT = os.getenv("DB_PORT")


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=BD_PORT
    )
    return conn


@app.route("/")
def index():
    return render_template("index.html")


# GET
@app.route("/api/clientes", methods=["GET"])
def get_clientes():
    try:
        params = []
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        search_text = request.args.get("search")
        search_type = request.args.get("type")
        print(f"Search: {search_text}, Type: {search_type}")
        query = "SELECT * FROM clientes"
        if search_text != None and search_type != None:
            if search_type == "igual":
                query += " WHERE razao_social = %s codigo = %s"
                params.append(search_text)
                params.append(search_text)

            elif search_type == "contendo":
                query += " WHERE razao_social ILIKE %s OR nome_fantasia ILIKE %s"
                term = f"%{search_text}%"
                params.append(term)
                params.append(term)

        query += " ORDER BY created_at DESC"
        print(f"Params: {params}")
        cur.execute(query, tuple(params))
        clientes = cur.fetchall()

        cur.close()
        conn.close()
        return jsonify(clientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST
@app.route("/api/clientes", methods=["POST"])
def create_cliente():
    data = request.json

    required_fields = ["codigo", "tipo_pessoa", "tipo_operacao", "razao_social"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Dados incompletos"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            INSERT INTO clientes 
            (codigo, tipo_pessoa, tipo_operacao, cpf_cnpj, inscricao_estadual, 
             razao_social, nome_fantasia, telefone, fax, regiao, email_nfe)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        cur.execute(
            query,
            (
                data["codigo"],
                data["tipo_pessoa"],
                data["tipo_operacao"],
                data.get("cpf_cnpj"),
                data.get("inscricao_estadual"),
                data["razao_social"],
                data.get("nome_fantasia"),
                data.get("telefone"),
                data.get("fax"),
                data.get("regiao"),
                data.get("email_nfe"),
            ),
        )

        new_id = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Cliente criado!", "id": new_id}), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "Erro: Código já existe."}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/empresas-select", methods=["GET"])
def get_empresas_select():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT id, razao_social FROM clientes ORDER BY razao_social ASC"

        cur.execute(query)
        empresas = cur.fetchall()

        cur.close()
        conn.close()
        return jsonify(empresas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
