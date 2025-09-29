# LLM Inference Frontend

A clean web interface for interacting with your deployed LLM service.

## Quick Start

### 1. Install Dependencies
```bash
pip install flask requests
```

### 2. Start the CORS Proxy Server
```bash
cd frontend
python cors-proxy.py
```

### 3. Open Your Browser
Visit: `http://localhost:3030`

## Features

- **Clean UI**: Modern gradient design with smooth animations
- **Real-time Responses**: Direct connection to your EKS-deployed LLM
- **Configurable Length**: Adjust response length 20-200 tokens
- **Copy to Clipboard**: Easy response sharing
- **Mobile Responsive**: Works on all devices

## Usage

1. Enter a prompt (e.g., "Tell me a joke")
2. Adjust response length with the slider
3. Click "Generate Response"
4. View AI-generated response

## API Connection

- **Proxy Endpoint**: `http://localhost:3030/proxy/generate`
- **EKS Service**: Automatically routes to your LoadBalancer
- **Model**: DialoGPT-medium running on Kubernetes

## Troubleshooting

### Server Not Starting
```bash
# Make sure you're in the frontend directory
cd frontend

# Install missing packages
pip install flask requests
```

### CORS Errors
- Use the provided proxy server (not direct file access)
- Server must be running on `localhost:3030`

### Connection Issues
- Verify EKS cluster: `kubectl get pods -n llm`
- Check proxy logs for error messages

## Files

- `index.html` - Main web interface
- `cors-proxy.py` - Flask proxy server with CORS headers
- `README.md` - This documentation
