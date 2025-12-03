# 🚀 Guia Rápido: Servidor LSTM

## ⚡ Início Rápido

### 1. Iniciar Servidor

```bash
./start_server.sh
```

Aguarde até ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 2. Testar API (em outro terminal)

```bash
./test_api.sh
```

Ou manualmente:

```bash
# Ativar ambiente
conda activate carbon-ai

# Testar
python test_forecast_endpoint.py
```

### 3. Acessar Documentação

Abra no navegador:
```
http://localhost:8000/docs
```

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'tensorflow'"

**Causa:** Servidor está usando o ambiente errado (venv em vez de carbon-ai)

**Solução:**
```bash
# Parar servidor (CTRL+C)
# Desativar venv
deactivate

# Usar o script
./start_server.sh
```

### Erro: "Model not found"

**Causa:** Arquivos do modelo não estão em `models/dl/`

**Solução:**
1. Baixe o modelo do Google Colab (veja `LSTM_INTEGRATION_GUIDE.md`)
2. Descompacte em `models/dl/`
3. Verifique: `ls -lh models/dl/`

### Erro: "Port 8000 already in use"

**Solução:**
```bash
# Encontrar processo
lsof -ti:8000

# Matar processo
kill -9 $(lsof -ti:8000)

# Reiniciar
./start_server.sh
```

---

## 📁 Estrutura de Arquivos

```
carbon-ai-microservice/
├── models/dl/
│   ├── lstm_energy_forecaster.keras    ← Modelo treinado
│   ├── scaler_X_lstm.pkl               ← Scaler de features
│   ├── scaler_y_lstm.pkl               ← Scaler de target
│   └── lstm_model_metadata.json        ← Metadados
├── src/api/
│   ├── main.py                         ← FastAPI app
│   └── endpoints/
│       └── forecast.py                 ← Endpoint LSTM
├── start_server.sh                     ← Script para iniciar servidor
├── test_api.sh                         ← Script para testar API
├── test_lstm_model.py                  ← Teste de carregamento
└── test_forecast_endpoint.py           ← Teste de endpoint
```

---

## 🎯 Endpoints Disponíveis

### GET `/api/forecast/info`
Retorna informações sobre o modelo LSTM

**Exemplo:**
```bash
curl http://localhost:8000/api/forecast/info
```

### POST `/api/forecast`
Faz previsão de consumo energético

**Exemplo:**
```bash
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d @examples/forecast_payload_example.json
```

---

## 📚 Documentação Completa

- **Guia de Integração:** `LSTM_INTEGRATION_GUIDE.md`
- **Documentação Interativa:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## ✅ Checklist

- [ ] Modelo baixado do Colab e descompactado em `models/dl/`
- [ ] Ambiente `carbon-ai` ativo
- [ ] Servidor iniciado com `./start_server.sh`
- [ ] Testes passando com `./test_api.sh`
- [ ] Documentação acessível em http://localhost:8000/docs
