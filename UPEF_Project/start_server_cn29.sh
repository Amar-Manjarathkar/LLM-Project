#!/bin/bash
# Optimized startup script for cn29 with 24 cores

# --- Configuration ---
NODE_NAME="cn29"
PORT=8000
WORKERS=20  # Safe bet for 24 free cores (leave 4 for OS/Ollama overhead)
LOG_DIR="logs"

# Ensure log directory exists
mkdir -p $LOG_DIR

# Set thread limits to avoid oversubscription
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

echo "=========================================="
echo "🚀 Starting UPEF Backend on $NODE_NAME"
echo "📅 Date: $(date)"
echo "CPU Cores Available: $(nproc)"
echo "Workers Configured: $WORKERS"
echo "=========================================="

# Navigate to project root
cd "$(dirname "$0")"

# Activate Virtual Environment
# We assume it's in the project root named 'venv'
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual Environment Activated"
else
    echo "❌ Error: 'venv' not found! Please create it first."
    exit 1
fi

# Check if Ollama is responsive
echo "🔍 Checking Ollama Status..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running."
else
    echo "⚠️  WARNING: Ollama might not be running locally on port 11434."
    echo "    Make sure 'ollama serve' is running in another terminal if needed."
fi

# Start Gunicorn with Uvicorn Workers
# --preload: load app code before forking (saves memory)
# --timeout 300: Allow 5 mins for LLM processing
echo "🔥 Firing up Gunicorn..."

nohup gunicorn server:app \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --timeout 300 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile "$LOG_DIR/access.log" \
    --error-logfile "$LOG_DIR/error.log" \
    --log-level info \
    --preload > "$LOG_DIR/startup.log" 2>&1 &

PID=$!
echo "✅ Server started in background with PID: $PID"
echo "📜 Logs: tail -f $LOG_DIR/error.log"
echo "🌐 Health Check: curl http://$(hostname):$PORT/"
