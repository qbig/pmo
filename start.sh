#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting PMO Assistant...${NC}"

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9+${NC}"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi

# Check for npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed. Please install npm${NC}"
    exit 1
fi

# Check LLM configuration
echo -e "${YELLOW}🤖 Checking LLM configuration...${NC}"
LLM_PROVIDER="${PMO_LLM_PROVIDER:-gemini}"
if [ "$LLM_PROVIDER" = "gemini" ]; then
    if [ -z "$PMO_LLM_API_KEY" ]; then
        echo -e "${YELLOW}⚠️  Warning: PMO_LLM_API_KEY is not set${NC}"
        echo -e "${YELLOW}   Gemini is the default LLM provider. Set PMO_LLM_API_KEY to use AI features.${NC}"
        echo -e "${YELLOW}   Get your API key from Google AI Studio.${NC}"
        echo -e "${YELLOW}   Or set PMO_LLM_PROVIDER=ollama or PMO_LLM_PROVIDER=openai to use alternatives${NC}"
        echo ""
    else
        echo -e "${GREEN}✅ Gemini API key found${NC}"
    fi
elif [ "$LLM_PROVIDER" = "ollama" ]; then
    echo -e "${YELLOW}ℹ️  Using Ollama (ensure Ollama is running)${NC}"
elif [ "$LLM_PROVIDER" = "openai" ]; then
    if [ -z "$PMO_LLM_API_KEY" ]; then
        echo -e "${YELLOW}⚠️  Warning: PMO_LLM_API_KEY is not set for OpenAI-compatible provider${NC}"
        echo ""
    else
        echo -e "${GREEN}✅ OpenAI API key found${NC}"
    fi
fi

echo -e "${YELLOW}📦 Setting up Python environment...${NC}"

# Create virtual environment if it doesn't exist
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip --quiet
pip install -r src/backend/requirements.txt --quiet

echo -e "${YELLOW}📦 Setting up Node.js environment...${NC}"

# Install Node dependencies
cd src/frontend
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies (this may take a minute)..."
    npm install
else
    echo "Node.js dependencies already installed, skipping..."
fi
cd "$SCRIPT_DIR"

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Shutdown complete${NC}"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup SIGINT SIGTERM

echo -e "${YELLOW}🔧 Starting backend server...${NC}"

# Start backend
export PMO_HOST="${PMO_HOST:-0.0.0.0}"
export PMO_PORT="${PMO_PORT:-8000}"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python3 -m src.backend.main &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s "http://127.0.0.1:${PMO_PORT}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Backend failed to start${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

echo -e "${YELLOW}🔧 Starting frontend server...${NC}"

# Start frontend
FRONTEND_HOST="${PMO_FRONTEND_HOST:-0.0.0.0}"
FRONTEND_PORT="${PMO_FRONTEND_PORT:-5173}"
FRONTEND_LOG="$SCRIPT_DIR/.frontend.log"
cd src/frontend
npm run dev -- --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" --strictPort > "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

# Wait for frontend to be ready
echo "Waiting for frontend to start..."
for i in {1..30}; do
    if curl -s "http://127.0.0.1:${FRONTEND_PORT}/" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend is ready${NC}"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Frontend failed to start${NC}"
        echo -e "${YELLOW}   See ${FRONTEND_LOG} for details${NC}"
        exit 1
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Frontend failed to start in time${NC}"
        echo -e "${YELLOW}   See ${FRONTEND_LOG} for details${NC}"
        exit 1
    fi
    sleep 1
done

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ PMO Assistant is running!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "🌐 Frontend: ${GREEN}http://localhost:${FRONTEND_PORT}${NC}"
echo -e "🔧 Backend API: ${GREEN}http://localhost:${PMO_PORT}${NC}"
echo -e "📊 Health Check: ${GREEN}http://localhost:${PMO_PORT}/health${NC}"
echo ""
if [ "$LLM_PROVIDER" = "gemini" ] && [ -z "$PMO_LLM_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Note: AI features require PMO_LLM_API_KEY to be set${NC}"
    echo ""
fi
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
