#!/bin/bash
# Startup script for GPU Node (gpu39) with Qwen 32B Model

# --- Configuration ---
NODE_NAME="gpu39"
PORT=8000
# For GPU inference, we only want 1 or 2 workers because the GPU is the bottleneck.
# Parallel requests would just queue up for the single GPU anyway.
WORKERS=2 
LOG_DIR="logs_gpu39"

# Ensure log directory exists
mkdir -p $LOG_DIR

echo "=========================================="
echo "🚀 Starting UPEF Backend on $NODE_NAME (GPU Mode)"
echo "🧠 Model: qwen2.5:32b"
echo "📅 Date: $(date)"
echo "Workers: $WORKERS"
echo "=========================================="

# Navigate to project root
cd "$(dirname "$0")"

# Activate Virtual Environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual Environment Activated"
else
    echo "❌ Error: 'venv' not found!"
    exit 1
fi

# Check if Ollama is responsive
echo "🔍 Checking Ollama Status..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running."
else
    echo "⚠️  WARNING: Ollama might not be running. Ensure 'ollama serve' is active."
fi

# Start Gunicorn
echo "🔥 Firing up Server..."

nohup gunicorn server:app \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --timeout 600 \
    --keep-alive 5 \
    --access-logfile "$LOG_DIR/access.log" \
    --error-logfile "$LOG_DIR/error.log" \
    --log-level info \
    --preload > "$LOG_DIR/startup.log" 2>&1 &

PID=$!
echo "✅ Server started in background with PID: $PID"
echo "📜 Logs: tail -f $LOG_DIR/error.log"
