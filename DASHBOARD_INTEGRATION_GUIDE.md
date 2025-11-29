# Dashboard Integration Guide
Integration steps for MyCarbonAI Dashboard + Carbon AI Microservice

## Prerequisites

1. **Carbon AI Microservice** running on port 8000
2. **MyCarbonAI Dashboard** codebase

---

## Step 1: Add ML Predictions Route to Dashboard

### Create new route file

Create: `/mycarbonai-dashboard/routes/ml-predictions.js`

**File already created** at: `/Users/nim/Dev/mycarbonai-dashboard/routes/ml-predictions.js`

---

## Step 2: Update Dashboard Server

Edit: `/mycarbonai-dashboard/server.js`

### Add import (after line 16):
```javascript
import mlPredictionsRoutes from './routes/ml-predictions.js';
```

### Add route (after line 74, before "STATIC FILES" section):
```javascript
// ML Predictions - AI microservice integration
app.use('/api/ml', mlPredictionsRoutes); // Protected: ML predictions and chatbot
```

---

## Step 3: Add Environment Variable

Edit: `/mycarbonai-dashboard/.env`

Add:
```
ML_SERVICE_URL=http://localhost:8000
```

---

## Step 4: Test Integration

### Start both services:

**Terminal 1 - ML Microservice:**
```bash
cd /Users/nim/Dev/ironhack/carbon-ai-microservice
./run_api.sh
```

**Terminal 2 - Dashboard:**
```bash
cd /Users/nim/Dev/mycarbonai-dashboard
npm run server:dev
```

### Test endpoints:

```bash
# Test ML service health (via dashboard proxy)
curl http://localhost:3000/api/ml/health

# Test energy prediction
curl -X POST http://localhost:3000/api/ml/predict/energy \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "building_id": 100,
    "square_feet": 50000,
    "primary_use": 0,
    "year_built": 2000,
    "floor_count": 5,
    "air_temperature": 22.5
  }'

# Test chatbot
curl -X POST http://localhost:3000/api/ml/chat/recommendations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "How can I reduce HVAC energy consumption?"
  }'
```

---

## Step 5: Frontend Integration (React)

### Create ML API Service

Create: `/mycarbonai-dashboard/src/services/mlService.js`

```javascript
// src/services/mlService.js
const API_BASE = '/api/ml';

export const mlService = {
  // Energy prediction
  async predictEnergy(buildingData) {
    const response = await fetch(`${API_BASE}/predict/energy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(buildingData)
    });

    if (!response.ok) {
      throw new Error('Energy prediction failed');
    }

    return response.json();
  },

  // Carbon emissions calculation
  async predictCarbon(energyData) {
    const response = await fetch(`${API_BASE}/predict/carbon`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(energyData)
    });

    if (!response.ok) {
      throw new Error('Carbon prediction failed');
    }

    return response.json();
  },

  // Full prediction pipeline
  async predictFull(buildingData) {
    const response = await fetch(`${API_BASE}/predict/full`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(buildingData)
    });

    if (!response.ok) {
      throw new Error('Full prediction failed');
    }

    return response.json();
  },

  // Chat with AI
  async chatRecommendations(message, context, conversationId) {
    const response = await fetch(`${API_BASE}/chat/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        message,
        context,
        conversation_id: conversationId
      })
    });

    if (!response.ok) {
      throw new Error('Chat failed');
    }

    return response.json();
  },

  // Get available topics
  async getTopics() {
    const response = await fetch(`${API_BASE}/chat/topics`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to get topics');
    }

    return response.json();
  },

  // Check ML service health
  async checkHealth() {
    const response = await fetch(`${API_BASE}/health`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    if (!response.ok) {
      throw new Error('ML service unhealthy');
    }

    return response.json();
  }
};
```

---

## Step 6: Example React Component

### Energy Prediction Component

```javascript
// src/components/EnergyPrediction.jsx
import React, { useState } from 'react';
import { mlService } from '../services/mlService';

export default function EnergyPrediction() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    building_id: 100,
    square_feet: 50000,
    primary_use: 0,
    year_built: 2000,
    floor_count: 5,
    air_temperature: 22.5,
    dew_temperature: 15.0,
    cloud_coverage: 3,
    wind_speed: 5.2,
    precip_depth_1_hr: 0,
    sea_level_pressure: 1013.25
  });

  const handlePredict = async () => {
    try {
      setLoading(true);
      setError(null);

      const result = await mlService.predictFull(formData);
      setPrediction(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Energy Prediction</h2>

      {/* Form inputs here */}

      <button
        onClick={handlePredict}
        disabled={loading}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {loading ? 'Predicting...' : 'Predict Energy'}
      </button>

      {prediction && (
        <div className="mt-4 p-4 bg-green-50 rounded">
          <h3 className="font-bold">Prediction Results:</h3>
          <p>Energy: {prediction.energy_prediction.predicted_energy_kwh} kWh</p>
          <p>Carbon: {prediction.carbon_emissions.carbon_emissions_kg} kg CO2e</p>
          <p>Confidence: {(prediction.energy_prediction.confidence_score * 100).toFixed(1)}%</p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-600 rounded">
          Error: {error}
        </div>
      )}
    </div>
  );
}
```

### AI Chatbot Component

```javascript
// src/components/AIChatbot.jsx
import React, { useState } from 'react';
import { mlService } from '../services/mlService';

export default function AIChatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await mlService.chatRecommendations(
        input,
        null,
        conversationId
      );

      setConversationId(response.conversation_id);

      const aiMessage = {
        role: 'assistant',
        content: response.response,
        sources: response.sources,
        recommendations: response.recommendations
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow h-96 flex flex-col">
      <div className="p-4 border-b">
        <h3 className="font-bold">AI Energy Advisor</h3>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded ${
              msg.role === 'user'
                ? 'bg-blue-100 ml-auto max-w-xs'
                : 'bg-gray-100 mr-auto max-w-md'
            }`}
          >
            <p className="text-sm">{msg.content}</p>
            {msg.sources && msg.sources.length > 0 && (
              <p className="text-xs text-gray-500 mt-2">
                Sources: {msg.sources.join(', ')}
              </p>
            )}
          </div>
        ))}
        {loading && <div className="text-gray-500">AI is thinking...</div>}
      </div>

      <div className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about energy efficiency..."
            className="flex-1 border rounded px-3 py-2"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## Step 7: Add to Dashboard Pages

### Update Insights Page

Edit: `/mycarbonai-dashboard/src/pages/Insights.jsx`

```javascript
import AIChatbot from '../components/AIChatbot';

// Add to the page:
<div className="col-span-12 lg:col-span-6">
  <AIChatbot />
</div>
```

### Add Predictions Page

Create: `/mycarbonai-dashboard/src/pages/Predictions.jsx`

```javascript
import EnergyPrediction from '../components/EnergyPrediction';

export default function Predictions() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">ML Predictions</h1>
      <EnergyPrediction />
    </div>
  );
}
```

---

## Architecture Diagram

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  React          │────────>│  Dashboard       │────────>│  ML Microservice│
│  Frontend       │  HTTP   │  Express Server  │  HTTP   │  (FastAPI)      │
│  (Port 5173)    │         │  (Port 3000)     │         │  (Port 8000)    │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                  │                             │
                                  │                             │
                                  v                             v
                            ┌──────────┐                 ┌──────────┐
                            │ Supabase │                 │ XGBoost  │
                            │ Database │                 │  Model   │
                            └──────────┘                 └──────────┘
                                                               │
                                                               v
                                                        ┌──────────┐
                                                        │    │
                                                        │   API    │
                                                        └──────────┘
```

---

## Testing Checklist

- [ ] ML Microservice running on port 8000
- [ ] Dashboard server running on port 3000
- [ ] Frontend running on port 5173
- [ ] `/api/ml/health` returns success
- [ ] Energy prediction works
- [ ] Carbon calculation works
- [ ] Chatbot responds
- [ ] Topics list loads
- [ ] UI components render
- [ ] Authentication works with ML routes

---

## Environment Variables Summary

### ML Microservice (.env)
```
PORT=8000
=your_key_here
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=false
```

### Dashboard (.env)
```
ML_SERVICE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

---

## Next Steps

1. Apply server.js changes
2. Test integration locally
3. Deploy ML microservice
4. Deploy dashboard
5. Update production URLs
