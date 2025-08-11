#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel serverless function entry point
"""

import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'scripts'))

try:
    # Import Flask app
    from web_server import app
    
    # Vercel handler function
    def handler(event, context):
        return app
        
    # Direct export for Vercel
    application = app
    
except Exception as e:
    print(f"Import error: {e}")
    # Fallback minimal Flask app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'error',
            'message': f'Import Error: {str(e)}',
            'suggestion': 'Please check the serverless function configuration'
        })
    
    @app.route('/api/segment', methods=['POST'])
    def segment():
        return jsonify({
            'success': False,
            'error': f'Import Error: {str(e)}'
        }), 500
    
    application = app