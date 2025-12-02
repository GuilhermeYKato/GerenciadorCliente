# Configuração do Python
## Visual Studio Code (VS Code)
1. Instalar a extensão **Python** no VS Code.
2. Abrir a barra de comandos do VS Code (Comando padrão: `Ctrl + Shift + P`). 
3. Digitar `Python: Create Environment` para criar um **ambiente virtual**.
4. Após criado, o VS Code deve ativar o ambiente automaticamente. Se não ativar, veja abaixo como fazer via terminal.
5. Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```


## Terminal
1. Crie o ambiente virtual para python:
```bash
python -m venv .venv
```

2. Ative o ambiente virtual:
    - **Windows:**
    ```bash
    ./.venv/Scripts/activate
    ```
    - **Linux/macOS:**
    ```bash
    source .venv/bin/activate
    ```

3. Instale os pacotes listados no arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

4. Para desativar o ambiente virtual:
```bash
deactivate
```
# Configurando o Tailwind
1. Baixe e instale o Node.js através do site oficial

2. Execute o seguinte comando na raz do projeto:
```bash
npm install
```

3. Se tudo instalou corretamente, você esta pronto para compilar o projeto

# Compilar o projeto

Com todas as dependências instaladas, compile e execute o arquivo `app.py` utilizando o comando abaixo:

```bash
python app.py
```

Abra outro terminal na raiz do projeto e execute:

```bash
npm run dev
```

Com Flask rodando e o Tailwind em modo dev, basta acessar:

```bash
http://localhost:5000
```