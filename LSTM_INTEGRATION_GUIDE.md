# Guia Passo a Passo: Integração do Modelo LSTM

## 📋 Pré-requisitos

- Notebook `lstm_forecasting_v2.ipynb` executado com sucesso no Google Colab
- Modelo treinado e métricas calculadas
- Acesso ao projeto local em `/Users/nim/Dev/ironhack/carbon-ai-microservice`

---

## 🔄 Fase 1: Exportar Modelo do Google Colab

### Passo 1.1: Adicionar Célula de Exportação

No **final do notebook** no Google Colab, adicione uma nova célula:

```python
import joblib
import json
import os
from google.colab import files

# Criar diretório para exportação
os.makedirs('lstm_model_export', exist_ok=True)

# 1. Salvar modelo treinado
model.save('lstm_model_export/lstm_energy_forecaster.keras')
print("✓ Modelo salvo: lstm_energy_forecaster.keras")

# 2. Salvar scalers
joblib.dump(scaler_X, 'lstm_model_export/scaler_X_lstm.pkl')
joblib.dump(scaler_y, 'lstm_model_export/scaler_y_lstm.pkl')
print("✓ Scalers salvos: scaler_X_lstm.pkl, scaler_y_lstm.pkl")

# 3. Salvar metadados
metadata = {
    'timesteps': TIMESTEPS,
    'features': feature_cols,
    'n_features': len(feature_cols),
    'rmse': float(rmse),
    'mae': float(mae),
    'mape': float(mape),
    'model_architecture': 'Bidirectional LSTM + Attention (128, 64 units)',
    'framework': 'TensorFlow/Keras 2.16.2',
    'training_samples': len(X_train_seq),
    'validation_samples': len(X_val_seq),
    'test_samples': len(X_test_seq),
    'trained_on': 'Google Colab',
    'date': '2025-12-03'
}

with open('lstm_model_export/lstm_model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print("✓ Metadados salvos: lstm_model_metadata.json")

print("\n📦 Arquivos prontos para download:")
for file in os.listdir('lstm_model_export'):
    size = os.path.getsize(f'lstm_model_export/{file}') / (1024*1024)
    print(f"  - {file} ({size:.2f} MB)")
```

**Execute esta célula** e verifique que todos os arquivos foram criados.

---

### Passo 1.2: Compactar e Baixar

Adicione outra célula:

```python
# Compactar em ZIP
!zip -r lstm_model_export.zip lstm_model_export/

# Baixar
files.download('lstm_model_export.zip')
```

**Execute** e o arquivo `lstm_model_export.zip` será baixado para `~/Downloads/`.

---

## 💾 Fase 2: Transferir para Projeto Local

### Passo 2.1: Descompactar no Diretório Correto

Abra o **terminal** e execute:

```bash
cd /Users/nim/Dev/ironhack/carbon-ai-microservice

# Criar diretório se não existir
mkdir -p models/dl

# Descompactar
unzip ~/Downloads/lstm_model_export.zip -d models/dl/

# Mover arquivos para models/dl/ (remover subdiretório)
mv models/dl/lstm_model_export/* models/dl/
rmdir models/dl/lstm_model_export
```

---

### Passo 2.2: Verificar Arquivos

```bash
ls -lh models/dl/
```

Você deve ver:

```
lstm_energy_forecaster.keras
scaler_X_lstm.pkl
scaler_y_lstm.pkl
lstm_model_metadata.json
```

---

### Passo 2.3: Testar Carregamento

Execute o script de teste que vou criar:

```bash
conda activate carbon-ai
python test_lstm_model.py
```

Se tudo estiver correto, você verá:

```
✓ Modelo carregado
✓ Scalers carregados
✓ Metadados carregados

📊 Informações do modelo:
  - Arquitetura: Bidirectional LSTM + Attention (128, 64 units)
  - Features: 15
  - Timesteps: 24
  - RMSE: [valor]
  - MAE: [valor]
  - MAPE: [valor]%

🧪 Teste de inferência...
✓ Predição de teste: 0.XXXX
```

---

## 🚀 Fase 3: Criar Endpoint FastAPI

### Passo 3.1: Criar Arquivo do Endpoint

O endpoint já foi criado em `src/api/endpoints/forecast.py`.

---

### Passo 3.2: Registrar no Router Principal

Verifique se `src/api/main.py` inclui o endpoint:

```python
from src.api.endpoints import forecast

app.include_router(forecast.router, prefix="/api", tags=["forecast"])
```

---

### Passo 3.3: Testar Endpoint Localmente

Inicie o servidor:

```bash
conda activate carbon-ai
uvicorn src.api.main:app --reload
```

Acesse a documentação interativa:

```
http://localhost:8000/docs
```

Teste o endpoint `/api/forecast` com um payload de exemplo.

---

## 📝 Fase 4: Documentação

### Passo 4.1: Atualizar TASK_TRACKING.md

Marque as tarefas como concluídas e adicione as métricas do modelo.

---

### Passo 4.2: Atualizar README.md

Adicione uma seção sobre o modelo LSTM e o endpoint de previsão.

---

### Passo 4.3: Commit e Push

```bash
git add .
git commit -m "feat: integrate LSTM forecasting model with FastAPI endpoint"
git push origin main
```

---

## ✅ Checklist Final

- [ ] Modelo exportado do Colab
- [ ] Arquivos transferidos para `models/dl/`
- [ ] Teste de carregamento passou
- [ ] Endpoint FastAPI criado
- [ ] Endpoint testado localmente
- [ ] Documentação atualizada
- [ ] Código commitado e pushed

---

## 🆘 Troubleshooting

### Erro: "No module named 'tensorflow'"

```bash
conda activate carbon-ai
pip install tensorflow
```

### Erro: "Cannot load model"

Verifique que o arquivo `.keras` está em `models/dl/` e não corrompido.

### Erro: "Shape mismatch"

Verifique que o número de features (15) e timesteps (24) estão corretos no payload.

---

## 📞 Próximos Passos

1. **Deploy**: Configurar deploy em produção (Heroku, AWS, GCP)
2. **Monitoramento**: Adicionar logging e métricas de performance
3. **Re-treinamento**: Configurar pipeline de re-treinamento periódico
4. **Otimização**: Converter para TensorFlow Lite para inferência mais rápida
