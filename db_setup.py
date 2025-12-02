import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
BD_PORT = os.getenv("DB_PORT")


def create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=BD_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        if not cur.fetchone():
            print(f"Criando banco de dados '{DB_NAME}'...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        else:
            print(f"Banco '{DB_NAME}' já existe.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro na criação do banco: {e}")


def run_migrations():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=BD_PORT,
        )
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS clientes CASCADE;")

        create_table_script = """
            CREATE TABLE clientes (
                id SERIAL PRIMARY KEY,
                codigo VARCHAR(50) NOT NULL UNIQUE,
                tipo_pessoa VARCHAR(1),
                tipo_operacao VARCHAR(20) ,
                cpf_cnpj VARCHAR(20),
                inscricao_estadual VARCHAR(30),
                razao_social VARCHAR(200) NOT NULL,
                nome_fantasia VARCHAR(200),
                telefone VARCHAR(20),
                fax VARCHAR(20),
                regiao VARCHAR(100),
                email_nfe VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """

        cur.execute(create_table_script)
        conn.commit()
        print("Tabela 'clientes' criada com sucesso.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro na migração: {e}")


if __name__ == "__main__":
    create_database()
    run_migrations()
