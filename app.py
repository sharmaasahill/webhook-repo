"""
TechStax Assessment - GitHub Webhook Receiver
This Flask application receives GitHub webhook events and stores them in MongoDB.
It also provides a web interface to display the latest repository activities.
"""

from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime, timezone
import hashlib
import hmac
import json
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'techstax_assessment')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'github_events')

# GitHub webhook secret
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-webhook-secret-key')

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

def verify_webhook_signature(payload_body, signature_header):
    """
    Verify GitHub webhook signature for security
    """
    if not signature_header:
        return False
    
    try:
        hash_object = hmac.new(
            WEBHOOK_SECRET.encode('utf-8'),
            payload_body,
            hashlib.sha256
        )
        expected_signature = "sha256=" + hash_object.hexdigest()
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception as e:
        logger.error(f"Error verifying webhook signature: {e}")
        return False

def parse_push_event(payload):
    """
    Parse GitHub push event payload
    """
    return {
        'request_id': payload.get('head_commit', {}).get('id', '')[:7],  # Short commit hash
        'author': payload.get('pusher', {}).get('name', 'Unknown'),
        'action': 'PUSH',
        'from_branch': '',  # Not applicable for push
        'to_branch': payload.get('ref', '').replace('refs/heads/', ''),
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

def parse_pull_request_event(payload):
    """
    Parse GitHub pull request event payload
    """
    pr = payload.get('pull_request', {})
    return {
        'request_id': str(pr.get('number', '')),
        'author': pr.get('user', {}).get('login', 'Unknown'),
        'action': 'PULL_REQUEST',
        'from_branch': pr.get('head', {}).get('ref', ''),
        'to_branch': pr.get('base', {}).get('ref', ''),
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

def parse_merge_event(payload):
    """
    Parse GitHub merge event payload (pull request merged)
    """
    pr = payload.get('pull_request', {})
    return {
        'request_id': str(pr.get('number', '')),
        'author': pr.get('merged_by', {}).get('login', 'Unknown'),
        'action': 'MERGE',
        'from_branch': pr.get('head', {}).get('ref', ''),
        'to_branch': pr.get('base', {}).get('ref', ''),
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """
    GitHub webhook endpoint to receive and process webhook events
    """
    try:
        # Get webhook signature for verification
        signature = request.headers.get('X-Hub-Signature-256')
        
        # Verify webhook signature (optional for development)
        if WEBHOOK_SECRET != 'your-webhook-secret-key':
            if not verify_webhook_signature(request.data, signature):
                logger.warning("Invalid webhook signature")
                return jsonify({'error': 'Invalid signature'}), 401

        # Get event type
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()

        if not payload:
            return jsonify({'error': 'No payload received'}), 400

        logger.info(f"Received webhook event: {event_type}")

        # Parse different event types
        event_data = None
        
        if event_type == 'push':
            event_data = parse_push_event(payload)
            
        elif event_type == 'pull_request':
            action = payload.get('action', '')
            if action == 'opened':
                event_data = parse_pull_request_event(payload)
            elif action == 'closed' and payload.get('pull_request', {}).get('merged'):
                # This is a merge event (brownie points!)
                event_data = parse_merge_event(payload)
                
        if event_data:
            # Store in MongoDB
            result = collection.insert_one(event_data)
            logger.info(f"Stored event with ID: {result.inserted_id}")
            
            return jsonify({
                'status': 'success',
                'message': f'{event_data["action"]} event processed successfully',
                'id': str(result.inserted_id)
            }), 200
        else:
            logger.info(f"Event type {event_type} not processed")
            return jsonify({
                'status': 'ignored',
                'message': f'Event type {event_type} not processed'
            }), 200

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/')
def index():
    """
    Main page displaying GitHub repository activities
    """
    return render_template('index.html')

@app.route('/api/events')
def get_events():
    """
    API endpoint to fetch latest GitHub events from MongoDB
    """
    try:
        # Fetch latest 50 events, sorted by timestamp (most recent first)
        events = list(collection.find().sort('timestamp', -1).limit(50))
        
        # Convert ObjectId to string for JSON serialization
        for event in events:
            event['_id'] = str(event['_id'])
        
        return jsonify({
            'status': 'success',
            'events': events,
            'count': len(events)
        })
        
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({'error': 'Failed to fetch events'}), 500

@app.route('/health')
def health_check():
    """
    Health check endpoint
    """
    try:
        # Test MongoDB connection
        collection.find_one()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting TechStax Webhook Receiver on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 