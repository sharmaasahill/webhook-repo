# GitHub Webhook Receiver

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-8.0+-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Ready-success.svg)

A professional Flask application that receives GitHub webhook events and displays them through a beautiful, real-time web interface. This project captures repository events (push, pull request, merge) in real-time and stores them in MongoDB for monitoring and analysis.

## Overview

This application serves as a webhook receiver for GitHub repository events. It processes incoming webhook payloads, stores event data in MongoDB, and provides a real-time dashboard to monitor repository activities. The dashboard automatically refreshes every 15 seconds to display the latest events.

## What This Project Does

- **Receives GitHub Webhooks**: Listens for push, pull request, and merge events from GitHub repositories
- **Stores Events in MongoDB**: Persists all events with structured data (author, branch, timestamp, etc.)
- **Real-time Dashboard**: Provides a web interface that displays events in real-time with auto-refresh
- **API Endpoints**: Exposes REST API endpoints to retrieve events programmatically
- **Health Monitoring**: Includes health check endpoint for monitoring application status

## Key Features

- **Real-time Event Monitoring** - Captures Push, Pull Request, and Merge events instantly
- **Beautiful Dashboard** - Modern, responsive web interface with live status indicators  
- **MongoDB Integration** - Persistent storage with optimized schema design
- **Webhook Security** - SHA-256 signature verification for production use
- **Mobile Responsive** - Works perfectly on desktop, tablet, and mobile devices
- **Auto-refresh** - Dashboard updates every 15 seconds automatically
- **Health Monitoring** - Built-in health checks and comprehensive logging
- **Event Formatting** - Professional display with color-coded event types

## Architecture

```
GitHub Repository
       ↓ Webhook Events
Flask Application (/webhook)
       ↓ Process & Store
MongoDB Database (github_webhook_db)
       ↓ Retrieve & Display  
Real-time Web Interface
```

## Supported Event Types

### Push Events
```
Format: {author} pushed to {branch} on {timestamp}
Example: "sahil.sharma pushed to main on Nov 9, 2025, 09:02 PM GMT+5:30"
```

### Pull Request Events
```
Format: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
Example: "sahil.sharma submitted a pull request from feature/auth to main on Nov 9, 2025, 09:01 PM GMT+5:30"
```

### Merge Events
```
Format: {author} merged branch {from_branch} to {to_branch} on {timestamp}
Example: "sahil.sharma merged branch feature/auth to main on Nov 9, 2025, 09:02 PM GMT+5:30"
```

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | Python Flask | 3.0.0 |
| **Database** | MongoDB | 8.0+ |
| **Frontend** | HTML5, CSS3, Vanilla JS | - |
| **Webhooks** | GitHub Webhooks API | v4 |
| **Tunneling** | ngrok | Latest |

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - `python --version`
- **MongoDB** - `mongod --version`  
- **Git** - `git --version`
- **ngrok** - `ngrok version` (for webhook testing)

## Installation

### Quick Setup (Using setup.sh)

```bash
# Run the setup script
bash setup.sh
```

The setup script will:
- Check Python and MongoDB installation
- Create virtual environment
- Install dependencies
- Create .env file from template

### Manual Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/sharmaasahill/webhook-repo.git
cd webhook-repo
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Create environment file from template
cp env.example .env

# Edit .env file with your configuration
# Key settings:
# - DATABASE_NAME=github_webhook_db
# - MONGO_URI=mongodb://localhost:27017/
# - PORT=5000
```

#### 5. Start MongoDB
```bash
# Windows: Start MongoDB service
net start MongoDB

# Or manually start MongoDB
mongod

# Verify MongoDB is running
mongosh --eval "db.runCommand('ping')"
```

## Running the Application

### Start the Flask Server
```bash
# Activate virtual environment (if not already activated)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Run the application
python app.py
```

You should see:
```
INFO:__main__:Successfully connected to MongoDB
INFO:__main__:Starting GitHub Webhook Receiver on port 5000
 * Running on http://0.0.0.0:5000
```

### Access the Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

### Expose with ngrok (for Webhook Testing)
```bash
# In a new terminal window
ngrok http 5000
```

You'll see output like:
```
Forwarding  https://xxxxx.ngrok.io -> http://localhost:5000
```

**Copy the HTTPS URL** - you'll need this for GitHub webhook configuration.

## GitHub Webhook Configuration

### Setup Instructions

1. **Navigate to Repository Settings**
   - Go to your GitHub repository
   - Click `Settings` → `Webhooks` → `Add webhook`

2. **Configure Webhook**
   ```
   Payload URL: https://your-ngrok-url.ngrok.io/webhook
   Content type: application/json
   Secret: (your webhook secret from .env file, optional)
   Events: Select "Push" and "Pull requests"
   Active: Yes
   ```

3. **Test the Integration**
   - Make a commit and push to your repository
   - Create a pull request
   - Merge a pull request
   - Watch events appear in real-time on the dashboard at `http://localhost:5000`

### Getting Your Payload URL

When you run `ngrok http 5000`, you'll see:
```
Forwarding  https://xxxxx.ngrok.io -> http://localhost:5000
```

Your payload URL will be: `https://xxxxx.ngrok.io/webhook`

**Important**: Always append `/webhook` to your ngrok URL when configuring the GitHub webhook.

## API Reference

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Web dashboard | HTML page |
| `/webhook` | POST | GitHub webhook receiver | JSON status |
| `/api/events` | GET | Retrieve all events | JSON array |
| `/health` | GET | Health check | JSON status |

### Example API Response
```json
{
  "status": "success",
  "events": [
    {
      "_id": "60f1b2c3d4e5f6789abc123",
      "request_id": "abc1234",
      "author": "sahil.sharma",
      "action": "PUSH",
      "from_branch": "",
      "to_branch": "main",
      "timestamp": "2025-11-09T09:02:30Z"
    }
  ],
  "count": 1
}
```

## Database Schema

Events are stored in MongoDB with the following structure:

```javascript
{
  "_id": ObjectId,           // Auto-generated MongoDB ID
  "request_id": "string",    // Git commit hash (short) or PR number
  "author": "string",        // GitHub username
  "action": "string",        // "PUSH", "PULL_REQUEST", or "MERGE"
  "from_branch": "string",   // Source branch (empty for push events)
  "to_branch": "string",     // Target branch  
  "timestamp": "string"      // ISO 8601 UTC datetime
}
```

### Database Information

- **Database Name**: `github_webhook_db`
- **Collection Name**: `github_events`
- **Connection**: MongoDB running on `localhost:27017` (default)

## Environment Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/` | Yes |
| `DATABASE_NAME` | Database name | `github_webhook_db` | Yes |
| `COLLECTION_NAME` | Collection name | `github_events` | Yes |
| `WEBHOOK_SECRET` | GitHub webhook secret | `your-webhook-secret-key` | Optional |
| `PORT` | Flask server port | `5000` | No |
| `DEBUG` | Enable debug mode | `False` | No |

### Example .env File
```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=github_webhook_db
COLLECTION_NAME=github_events

# GitHub Webhook Secret
WEBHOOK_SECRET=your-webhook-secret-key

# Flask Configuration
PORT=5000
DEBUG=False
```

## Project Structure

```
webhook-repo/
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # Web interface template
├── requirements.txt       # Python dependencies
├── env.example           # Environment configuration template
├── setup.sh             # Automated setup script
├── .gitignore           # Git ignore rules
└── README.md            # This documentation
```

## Testing

### Manual Testing
```bash
# 1. Health check
curl http://localhost:5000/health

# 2. API endpoint
curl http://localhost:5000/api/events

# 3. Webhook endpoint (test)
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Integration Testing
1. **Push Event**: Make a commit to connected repository
2. **Pull Request**: Create a PR from feature branch
3. **Merge Event**: Merge the PR
4. **Real-time Verification**: Watch events appear on dashboard

## Troubleshooting

### MongoDB Connection Issues
**Problem**: `Failed to connect to MongoDB`

**Solutions**:
- Ensure MongoDB is running: `mongod --version`
- Check your `MONGO_URI` in `.env` file
- For MongoDB Atlas: Use full connection string with credentials
- For local MongoDB: Ensure service is started
- Windows: `net start MongoDB`

### Webhook Not Receiving Events
**Problem**: GitHub webhook returns 404 or timeout

**Solutions**:
- Verify ngrok is running: `ngrok http 5000`
- Check webhook URL includes `/webhook` endpoint
- Ensure Flask app is running on port 5000
- Check GitHub webhook delivery logs
- Verify payload URL format: `https://xxxxx.ngrok.io/webhook`

### UI Not Updating
**Problem**: Dashboard shows old data

**Solutions**:
- Check browser console for JavaScript errors
- Verify `/api/events` endpoint responds: `curl http://localhost:5000/api/events`
- Clear browser cache and reload
- Check MongoDB connection status

### Port Already in Use
**Problem**: `Address already in use` on port 5000

**Solutions**:
- Change port in `.env`: `PORT=5001`
- Or kill process using port 5000:
  ```bash
  # Windows:
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

## Development

### Code Structure
- `app.py`: Main Flask application with webhook processing logic
- `templates/index.html`: Frontend dashboard with real-time updates
- Event parsing functions handle different GitHub event types
- MongoDB integration for persistent storage

### Key Functions
- `parse_push_event()`: Parses GitHub push event payloads
- `parse_pull_request_event()`: Parses GitHub pull request event payloads
- `parse_merge_event()`: Parses GitHub merge event payloads
- `verify_webhook_signature()`: Verifies webhook signature for security



## Contributing

For questions or improvements:

1. **Issues**: Report bugs or feature requests
2. **Pull Requests**: Improvements welcome
3. **Contact**: Technical queries via email at i.sahilkrsharma@gmail.com

## License

This project is created for personal use and educational purposes.

---

<div align="left">

**GitHub Webhook Receiver**

*Demonstrating full-stack development, real-time web applications, and professional software engineering practices*

![Made with Python](https://img.shields.io/badge/Built%20with-Python-blue.svg)

</div>
