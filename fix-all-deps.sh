#!/bin/bash

# 🔧 Complete fix for TensorFlow + NumPy + SciPy compatibility
# This fixes the "All ufuncs must have type numpy.ufunc" error

echo "🔧 Fixing package compatibility in carbon-ai environment..."
echo ""

# Initialize conda
eval "$(conda shell.bash hook)"
conda activate carbon-ai

echo "📦 Current versions:"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')" 2>/dev/null
python -c "import scipy; print(f'SciPy: {scipy.__version__}')" 2>/dev/null

echo ""
echo "⬇️  Installing compatible versions..."
echo "   - NumPy 1.26.4"
echo "   - SciPy 1.11.4"
echo ""

# Install compatible versions
pip install "numpy==1.26.4" "scipy==1.11.4" --force-reinstall

echo ""
echo "✅ Testing imports..."

python << 'PYTEST'
try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except Exception as e:
    print(f"❌ NumPy: {e}")

try:
    import scipy
    print(f"✅ SciPy {scipy.__version__}")
except Exception as e:
    print(f"❌ SciPy: {e}")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__}")
except Exception as e:
    print(f"❌ TensorFlow: {e}")

try:
    import lightgbm as lgb
    print(f"✅ LightGBM {lgb.__version__}")
except Exception as e:
    print(f"❌ LightGBM: {e}")
PYTEST

echo ""
echo "🎉 Done! Now start the server:"
echo "   conda activate carbon-ai"
echo "   uvicorn src.api.main:app --reload --port 8000"
echo ""
