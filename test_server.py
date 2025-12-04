#!/usr/bin/env python3
"""
Script de teste para verificar se todos os módulos estão carregando corretamente.
"""
import sys

print("=" * 60)
print("Testando imports do servidor...")
print("=" * 60)

# 1. TensorFlow
print("\n1. TensorFlow...")
try:
    import tensorflow as tf
    print(f"   ✓ TensorFlow {tf.__version__}")
except Exception as e:
    print(f"   ⚠️  TensorFlow: {e}")

# 2. LightGBM
print("\n2. LightGBM...")
try:
    import lightgbm as lgb
    print(f"   ✓ LightGBM {lgb.__version__}")
except Exception as e:
    print(f"   ❌ LightGBM: {e}")
    sys.exit(1)

# 3. FastAPI
print("\n3. FastAPI...")
try:
    import fastapi
    print(f"   ✓ FastAPI {fastapi.__version__}")
except Exception as e:
    print(f"   ❌ FastAPI: {e}")
    sys.exit(1)

# 4. OpenAI
print("\n4. OpenAI...")
try:
    import openai
    print(f"   ✓ OpenAI {openai.__version__}")
except Exception as e:
    print(f"   ⚠️  OpenAI: {e}")

# 5. NumPy/SciPy
print("\n5. NumPy/SciPy...")
try:
    import numpy as np
    import scipy
    print(f"   ✓ NumPy {np.__version__}")
    print(f"   ✓ SciPy {scipy.__version__}")
except Exception as e:
    print(f"   ❌ NumPy/SciPy: {e}")
    sys.exit(1)

# 6. Carregar modelos
print("\n6. Carregando modelos...")
import os

# LightGBM
if os.path.exists('models/lightgbm_energy_model.txt'):
    print("   ✓ LightGBM model encontrado")
else:
    print("   ⚠️  LightGBM model não encontrado")

# LSTM (opcional)
if os.path.exists('models/dl/lstm_energy_forecaster.keras'):
    print("   ✓ LSTM model encontrado")
else:
    print("   ⚠️  LSTM model não encontrado (opcional)")

print("\n" + "=" * 60)
print("✓ Servidor pronto para iniciar!")
print("Execute: uvicorn src.api.main:app --reload --port 8000")
print("=" * 60)
