# Projeto de Processamento Gráfico


## Como executar o projeto

### Pré-requisitos

Para executar o projeto, é necessário ter instalado o Python 3.7. Além disso, é necessário instalar as bibliotecas listadas em `requirements.txt`. Para isso, execute o seguinte comando:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Executando o projeto

Para executar o projeto, execute o seguinte comando:

```bash
python -m src.main
```

### Executando os testes

Para executar os testes, execute o seguinte comando:

```bash
pytest --cov=src tests/
```