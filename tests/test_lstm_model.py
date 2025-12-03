"""
Script de teste para verificar o carregamento do modelo LSTM.
"""
import tensorflow as tf
import joblib
import json
import numpy as np
import os

def test_model_loading():
    """Testa o carregamento do modelo, scalers e metadados."""
    
    print("🔍 Verificando arquivos...")
    
    # Verificar existência dos arquivos
    required_files = [
        'models/dl/lstm_energy_forecaster.keras',
        'models/dl/scaler_X_lstm.pkl',
        'models/dl/scaler_y_lstm.pkl',
        'models/dl/lstm_model_metadata.json'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Arquivo não encontrado: {file}")
            return False
        else:
            size = os.path.getsize(file) / (1024*1024)
            print(f"✓ {file} ({size:.2f} MB)")
    
    print("\n📥 Carregando modelo...")
    
    try:
        # Carregar modelo
        model = tf.keras.models.load_model('models/dl/lstm_energy_forecaster.keras')
        print("✓ Modelo carregado com sucesso")
        
        # Carregar scalers
        scaler_X = joblib.load('models/dl/scaler_X_lstm.pkl')
        scaler_y = joblib.load('models/dl/scaler_y_lstm.pkl')
        print("✓ Scalers carregados com sucesso")
        
        # Carregar metadados
        with open('models/dl/lstm_model_metadata.json', 'r') as f:
            metadata = json.load(f)
        print("✓ Metadados carregados com sucesso")
        
        # Exibir informações
        print(f"\n📊 Informações do modelo:")
        print(f"  - Arquitetura: {metadata.get('model_architecture', 'N/A')}")
        print(f"  - Features: {metadata.get('n_features', 'N/A')}")
        print(f"  - Timesteps: {metadata.get('timesteps', 'N/A')}")
        print(f"  - RMSE: {metadata.get('rmse', 0):.2f}")
        print(f"  - MAE: {metadata.get('mae', 0):.2f}")
        print(f"  - MAPE: {metadata.get('mape', 0):.2f}%")
        print(f"  - Framework: {metadata.get('framework', 'N/A')}")
        print(f"  - Treinado em: {metadata.get('trained_on', 'N/A')}")
        
        # Teste de inferência
        print("\n🧪 Teste de inferência...")
        timesteps = metadata.get('timesteps', 24)
        n_features = metadata.get('n_features', 15)
        
        dummy_input = np.random.rand(1, timesteps, n_features)
        prediction = model.predict(dummy_input, verbose=0)
        
        print(f"✓ Predição de teste (escala normalizada): {prediction[0][0]:.4f}")
        
        # Inverter escala
        pred_log = scaler_y.inverse_transform(prediction)[0][0]
        pred_original = np.expm1(pred_log)
        
        print(f"✓ Predição de teste (escala log): {pred_log:.4f}")
        print(f"✓ Predição de teste (escala original): {pred_original:.2f}")
        
        print("\n✅ Todos os testes passaram!")
        print("\n📝 Próximo passo: Execute 'uvicorn src.api.main:app --reload' para testar o endpoint")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao carregar modelo: {e}")
        return False

if __name__ == "__main__":
    test_model_loading()
