#!/bin/bash

# 🔧 Fix NumPy compatibility issue for TensorFlow in carbon-ai environment
# TensorFlow 2.16 requires NumPy <2.0

echo "🔧 Fixing NumPy compatibility for TensorFlow in carbon-ai..."
echo ""

# Initialize conda
eval "$(conda shell.bash hook)"

# Activate carbon-ai environment
echo "📦 Activating carbon-ai environment..."
conda activate carbon-ai

# Check current NumPy version
echo ""
echo "🔍 Current versions:"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')" 2>/dev/null || echo "NumPy not found"
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')" 2>/dev/null || echo "TensorFlow not found"

echo ""
echo "⬇️  Downgrading NumPy to 1.26.4 (compatible with TensorFlow 2.16)..."
pip install "numpy==1.26.4" --force-reinstall

echo ""
echo "✅ Verifying installation..."
python -c "import numpy; print(f'✓ NumPy: {numpy.__version__}')"
python -c "import tensorflow as tf; print(f'✓ TensorFlow: {tf.__version__}')"

echo ""
echo "🎉 Fixed! Now restart the FastAPI server:"
echo "   conda activate carbon-ai"
echo "   uvicorn src.api.main:app --reload --port 8000"
echo ""
