#!/bin/bash

# Script para iniciar o servidor FastAPI com o ambiente correto

echo "🚀 Iniciando servidor FastAPI com ambiente carbon-ai..."

# Desativar venv se estiver ativo
if [ -n "$VIRTUAL_ENV" ]; then
    echo "⚠️  Desativando venv..."
    deactivate 2>/dev/null || true
fi

# Ativar ambiente conda
echo "✓ Ativando ambiente carbon-ai..."
eval "$(conda shell.bash hook)"
conda activate carbon-ai

# Verificar se TensorFlow está disponível
echo "🔍 Verificando TensorFlow..."
python -c "import tensorflow as tf; print(f'✓ TensorFlow {tf.__version__} disponível')" || {
    echo "❌ TensorFlow não encontrado!"
    exit 1
}

# Verificar se modelo existe
if [ ! -f "models/dl/lstm_energy_forecaster.keras" ]; then
    echo "⚠️  Modelo LSTM não encontrado em models/dl/"
    echo "   Execute o guia LSTM_INTEGRATION_GUIDE.md primeiro"
fi

# Iniciar servidor
echo ""
echo "🌐 Iniciando servidor em http://127.0.0.1:8000"
echo "📚 Documentação: http://127.0.0.1:8000/docs"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo ""

uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
