@echo off
setlocal

if "%WATSONX_PROJECT_ID%"=="" (
  echo Set WATSONX_PROJECT_ID before running this script.
  exit /b 1
)

if "%WATSONX_API_KEY%"=="" (
  echo Set WATSONX_API_KEY before running this script.
  exit /b 1
)

ibmcloud ce secret create --name pitmind-secrets --format generic ^
  --from-literal BACKEND_CORS_ORIGINS="%BACKEND_CORS_ORIGINS%" ^
  --from-literal RATE_LIMIT_PER_MINUTE="%RATE_LIMIT_PER_MINUTE%" ^
  --from-literal WATSONX_URL="%WATSONX_URL%" ^
  --from-literal WATSONX_PROJECT_ID="%WATSONX_PROJECT_ID%" ^
  --from-literal WATSONX_API_KEY="%WATSONX_API_KEY%" ^
  --from-literal WATSONX_MODEL_ID="%WATSONX_MODEL_ID%" ^
  --from-literal LANGFLOW_API_URL="%LANGFLOW_API_URL%" ^
  --from-literal LANGFLOW_FLOW_ID="%LANGFLOW_FLOW_ID%" ^
  --from-literal LANGFLOW_API_KEY="%LANGFLOW_API_KEY%" ^
  --from-literal VITE_FIREBASE_API_KEY="%VITE_FIREBASE_API_KEY%" ^
  --from-literal VITE_FIREBASE_AUTH_DOMAIN="%VITE_FIREBASE_AUTH_DOMAIN%" ^
  --from-literal VITE_FIREBASE_PROJECT_ID="%VITE_FIREBASE_PROJECT_ID%" ^
  --from-literal VITE_FIREBASE_STORAGE_BUCKET="%VITE_FIREBASE_STORAGE_BUCKET%" ^
  --from-literal VITE_FIREBASE_MESSAGING_SENDER_ID="%VITE_FIREBASE_MESSAGING_SENDER_ID%" ^
  --from-literal VITE_FIREBASE_APP_ID="%VITE_FIREBASE_APP_ID%" ^
  --from-literal VITE_FIREBASE_DATABASE_URL="%VITE_FIREBASE_DATABASE_URL%" ^
  --from-literal FIREBASE_PROJECT_ID="%FIREBASE_PROJECT_ID%" ^
  --from-literal ENVIRONMENT="%ENVIRONMENT%" ^
  --from-literal VITE_API_BASE_URL="%VITE_API_BASE_URL%" ^
  --from-literal POSTGRES_PASSWORD="%POSTGRES_PASSWORD%" ^
  --from-literal REDIS_PASSWORD="%REDIS_PASSWORD%"
