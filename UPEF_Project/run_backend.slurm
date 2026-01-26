#!/bin/bash
#SBATCH --job-name=fastapi_backend
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=64G
#SBATCH --time=4-00:00:00
#SBATCH --output=backend_%j.log
#SBATCH --error=backend_%j.err

# Load any required modules (adjust based on your cluster setup)
# module load python/3.9  # Uncomment if needed

# Set environment variables
export OMP_NUM_THREADS=48
export MKL_NUM_THREADS=48
export NUMEXPR_NUM_THREADS=48

# Navigate to your project directory
cd $SLURM_SUBMIT_DIR

# Activate virtual environment if you have one
# source venv/bin/activate  # Uncomment if needed

# Get node hostname for logging
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
echo "Starting FastAPI backend with 48 workers..."

# Run the backend with Gunicorn using 48 worker processes
# Each worker will handle requests independently
gunicorn server:app \
    --workers 48 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 300 \
    --access-logfile backend_access.log \
    --error-logfile backend_error.log \
    --log-level info

# Note: 48 workers might be overkill. Start with 8-16 and scale up based on load
