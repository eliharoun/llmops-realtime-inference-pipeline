#!/usr/bin/env python3
"""
Simple CORS proxy for LLM Frontend - allows browser access to EKS service
"""
from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

# EKS LoadBalancer endpoint
EKS_ENDPOINT = "http://ad31829ed8a434db4b1a078eac5f0ac8-36229096.us-east-1.elb.amazonaws.com"

@app.route('/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/proxy/', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path=""):
    """Proxy requests to EKS with CORS headers"""

    # Handle OPTIONS for CORS preflight
    if request.method == 'OPTIONS':
        response = Response()
        response.status_code = 200
    else:
        # Forward the request to EKS
        target_url = f"{EKS_ENDPOINT}/{path}" if path else EKS_ENDPOINT

        try:
            # Forward the request
            resp = requests.request(
                method=request.method,
                url=target_url,
                headers={k: v for k, v in request.headers if k.lower() not in ['host', 'content-length']},
                data=request.get_data(),
                params=request.args,
                timeout=30
            )

            # Create response with CORS headers
            response = Response(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get('content-type', 'application/json')
            )

        except Exception as e:
            # Handle errors gracefully
            error_data = {'error': str(e), 'status': 'error'}
            response = Response(
                json.dumps(error_data),
                status=500,
                content_type='application/json'
            )

    # Add CORS headers to ALL responses
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Max-Age': '3600'
    })

    return response

@app.route('/', methods=['GET'])
def index():
    """Serve the frontend"""
    return app.send_static_file('index.html')

if __name__ == '__main__':
    print("🚀 CORS Proxy Server Starting...")
    print("📄 Frontend: http://localhost:3030")
    print("🔧 EKS Proxy: http://localhost:3030/proxy/generate")
    print()
    print("Press Ctrl+C to stop")

    app.run(host='127.0.0.1', port=3030, debug=True)
