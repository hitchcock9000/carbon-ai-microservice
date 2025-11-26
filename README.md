# Carbon AI Microservice

## Overview
This repository contains the **Carbon AI Microservice**, a backend service designed to process, analyze, and predict building energy consumption using machine learning techniques. The goal is to provide insights into carbon footprints and support sustainable decisions.

## Project Structure
- `src/` – Main source code of the microservice.
- `data/` – Raw, processed, and external data (not versioned).
- `notebooks/` – Jupyter notebooks for data exploration (EDA) and preprocessing.
- `models/` – Trained models (not versioned).
- `tests/` – Unit and integration tests.
- `docker/` – Docker configuration for containerization.

## Installation
```bash
# Clone the repository
git clone https://github.com/hitchcock9000/carbon-ai-microservice.git
cd carbon-ai-microservice

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage
1. **Preprocessing** – Run the notebook `notebooks/02_preprocessing/data_preprocessing.ipynb` to clean and transform the data.
2. **Training** – Use the scripts in `src/models/` to train ML/DL models.
3. **API** – Start the API with:
   ```bash
   uvicorn src.api:app --reload
   ```
   The API exposes endpoints to predict consumption and calculate carbon emissions.

## Tests
```bash
pytest
```

## Contributing
- Create a branch from `main`.
- Commit your changes.
- Open a Pull Request for review.

## License
This project is licensed under the MIT License.

*This README is a work in progress and will be updated incrementally as the project evolves.*

## Visão Geral
Este repositório contém o **Carbon AI Microservice**, um serviço backend desenvolvido para processar, analisar e prever o consumo de energia de edifícios usando técnicas de aprendizado de máquina. O objetivo é fornecer insights sobre a pegada de carbono e apoiar decisões sustentáveis.

## Estrutura do Projeto
- `src/` – Código‑fonte principal do microserviço.
- `data/` – Dados brutos, processados e externos (não versionados).
- `notebooks/` – Jupyter notebooks para exploração de dados (EDA) e pré‑processamento.
- `models/` – Modelos treinados (não versionados).
- `tests/` – Testes unitários e de integração.
- `docker/` – Configurações Docker para containerização.

## Instalação
```bash
# Clone o repositório
git clone https://github.com/hitchcock9000/carbon-ai-microservice.git
cd carbon-ai-microservice

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Uso
1. **Pré‑processamento** – Execute o notebook `notebooks/02_preprocessing/data_preprocessing.ipynb` para limpar e transformar os dados.
2. **Treinamento** – Use os scripts em `src/models/` para treinar os modelos de ML/DL.
3. **API** – Inicie a API com:
   ```bash
   uvicorn src.api:app --reload
   ```
   A API expõe endpoints para predizer consumo e calcular emissões de carbono.

## Testes
```bash
pytest
```

## Contribuição
- Crie uma branch a partir de `main`.
- Faça commit das suas alterações.
- Abra um Pull Request para revisão.

## Licença
Este projeto está licenciado sob a licença MIT.
