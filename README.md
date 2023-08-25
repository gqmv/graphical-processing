# Projeto de Processamento Gráfico


## Como executar o projeto

### Pré-requisitos

Para executar o projeto, é necessário ter instalado o Python 3.7. Além disso, é necessário instalar as bibliotecas listadas em `requirements.txt`. Para isso, execute o seguinte comando:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Criando cenas

Para criar cenas, é necessário utilizar o comando a seguir:
    
```bash
python -m src.scene_manager [arquivo_destino]
```

Onde `[arquivo_destino]` é o caminho para o arquivo que será criado. O arquivo será criado no formato JSON.

OBS: Em caso de dúvidas, execute o comando `python -m src.scene_creator --help` para mais informações.

### Renderizando cenas

Para renderizar cenas, é necessário utilizar o comando a seguir:

```bash
python -m src.renderer [arquivo_cena] [arquivo_imagem]
```

Onde `[arquivo_cena]` é o caminho para o arquivo que será renderizado e `[arquivo_imagem]` é o caminho para o arquivo que será criado. O arquivo será criado no formato PNG.

OBS: Em caso de dúvidas, execute o comando `python -m src.main --help` para mais informações.


### Editando cenas

Para editar cenas, é necessário utilizar o comando a seguir:

```bash
python -m src.scene_manager -e [arquivo_cena]
```

Onde `[arquivo_cena]` é o caminho para o arquivo que será editado.


### Exemplos

Cenas de exemplo podem ser encontradas na pasta `demos`. Para renderizar uma cena de exemplo, basta executar o comando a seguir:

```bash
python -m src.renderer demo/[arquivo_cena] [arquivo_imagem]
```

Onde `[arquivo_cena]` é o nome do arquivo que será renderizado e `[arquivo_imagem]` é o caminho para o arquivo que será criado. O arquivo será criado no formato PPM.