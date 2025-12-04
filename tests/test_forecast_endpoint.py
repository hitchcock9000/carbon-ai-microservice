"""
Script para testar o endpoint de previsão LSTM.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_model_info():
    """Testa o endpoint de informações do modelo."""
    print("🔍 Testando endpoint /api/forecast/info...")
    
    response = requests.get(f"{BASE_URL}/api/forecast/info")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Endpoint funcionando")
        print(f"\n📊 Informações do modelo:")
        print(f"  - Arquitetura: {data.get('architecture')}")
        print(f"  - Timesteps: {data.get('timesteps')}")
        print(f"  - Features: {data.get('n_features')}")
        print(f"  - RMSE: {data.get('metrics', {}).get('rmse'):.2f}")
        print(f"  - MAE: {data.get('metrics', {}).get('mae'):.2f}")
        print(f"  - MAPE: {data.get('metrics', {}).get('mape'):.2f}%")
        return True
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)
        return False

def test_forecast():
    """Testa o endpoint de previsão."""
    print("\n🔮 Testando endpoint /api/forecast...")
    
    # Carregar payload de exemplo
    with open('examples/forecast_payload_example.json', 'r') as f:
        payload = json.load(f)
    
    # Remover descrição (não faz parte do payload real)
    if 'features_description' in payload:
        del payload['features_description']
    if 'description' in payload:
        del payload['description']
    
    response = requests.post(
        f"{BASE_URL}/api/forecast",
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Previsão realizada com sucesso")
        print(f"\n📈 Resultado:")
        print(f"  - Previsão (escala original): {data.get('prediction'):.2f}")
        print(f"  - Previsão (escala log): {data.get('prediction_log'):.4f}")
        print(f"\n🤖 Modelo usado:")
        model_info = data.get('model_info', {})
        print(f"  - Arquitetura: {model_info.get('architecture')}")
        print(f"  - RMSE: {model_info.get('rmse'):.2f}")
        print(f"  - MAE: {model_info.get('mae'):.2f}")
        return True
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)
        return False

def test_invalid_payload():
    """Testa validação de payload inválido."""
    print("\n🧪 Testando validação de payload inválido...")
    
    # Payload com shape errado
    invalid_payload = {
        "sequence": [[1, 2, 3]]  # Shape errado
    }
    
    response = requests.post(
        f"{BASE_URL}/api/forecast",
        json=invalid_payload
    )
    
    if response.status_code == 400:
        print("✓ Validação funcionando (erro esperado)")
        return True
    else:
        print(f"❌ Validação não funcionou corretamente: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🚀 Testando API de Previsão LSTM\n")
    print("=" * 60)
    
    # Verificar se servidor está rodando
    try:
        requests.get(BASE_URL)
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando!")
        print("\nInicie o servidor com:")
        print("  conda activate carbon-ai")
        print("  uvicorn src.api.main:app --reload")
        exit(1)
    
    # Executar testes
    results = []
    
    results.append(("Info Endpoint", test_model_info()))
    results.append(("Forecast Endpoint", test_forecast()))
    results.append(("Validation", test_invalid_payload()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 Resumo dos Testes:\n")
    
    for test_name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✅ Todos os testes passaram!")
    else:
        print("\n❌ Alguns testes falharam. Verifique os logs acima.")
