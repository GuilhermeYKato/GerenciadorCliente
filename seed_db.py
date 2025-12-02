import psycopg2
import random
from faker import Faker
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
BD_PORT = os.getenv("DB_PORT")

# Gera dados falsos
fake = Faker("pt_BR")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=BD_PORT
    )


def gerar_dados_fakes(quantidade=10):
    conn = get_db_connection()
    cur = conn.cursor()

    print(f"--- Iniciando a inserção de {quantidade} clientes ---")

    for i in range(quantidade):
        tipo_pessoa = "J"
        razao_social = fake.company()
        nome_fantasia = razao_social.split(" ")[0] + " " + fake.company_suffix()
        cpf_cnpj = fake.cpf()
        inscricao_estadual = str(random.randint(100000000, 999999999))
        codigo = str(random.randint(1000, 999999))
        tipo_operacao = random.choice(["Venda", "Servico"])
        telefone = fake.phone_number()
        email = fake.email()
        regiao = fake.state_abbr()
        fax = None

        query = """
            INSERT INTO clientes 
            (codigo, tipo_pessoa, tipo_operacao, cpf_cnpj, inscricao_estadual, 
             razao_social, nome_fantasia, telefone, fax, regiao, email_nfe)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cur.execute(
                query,
                (
                    codigo,
                    tipo_pessoa,
                    tipo_operacao,
                    cpf_cnpj,
                    inscricao_estadual,
                    razao_social,
                    nome_fantasia,
                    telefone,
                    None,
                    regiao,
                    email,
                ),
            )
            print(f"Inserido: {razao_social} ({tipo_pessoa})")

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print(f"X Duplicidade de código {codigo} ignorada.")
            continue
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir: {e}")
            continue

    conn.commit()
    cur.close()
    conn.close()
    print("--- Processo finalizado! ---")


if __name__ == "__main__":
    gerar_dados_fakes(40)
