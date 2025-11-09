# GitHub Webhook Receiver

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-8.0+-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Ready-success.svg)

A professional Flask application that receives GitHub webhook events and displays them through a beautiful, real-time web interface.

## Live Demo

Visit the web interface at `http://localhost:5000` after setup to see real-time GitHub events flowing in automatically every 15 seconds.

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
MongoDB Database
       ↓ Retrieve & Display  
Real-time Web Interface
```

## Supported Event Types

### Push Events
```
Format: {author} pushed to {branch} on {timestamp}
Example: "john.doe pushed to main on Jul 2, 2025, 04:02 AM GMT+5:30"
```

### Pull Request Events
```
Format: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
Example: "jane.smith submitted a pull request from feature/auth to main on Jul 2, 2025, 04:01 AM GMT+5:30"
```

### Merge Events
```
Format: {author} merged branch {from_branch} to {to_branch} on {timestamp}
Example: "john.doe merged branch feature/auth to main on Jul 2, 2025, 04:02 AM GMT+5:30"
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

## Quick Start

### Clone & Setup
```bash
# Clone this repository
git clone https://github.com/sharmaasahill/webhook-repo.git
cd webhook-repo

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup
```bash
# Start MongoDB
mongod

# Verify connection (optional)
mongosh --eval "db.runCommand('ping')"
```

### Configuration
```bash
# Create environment file
cp env.example .env

# Edit configuration (optional)
# Set your MongoDB URI and webhook secret
```

### Launch Application
```bash
# Start the Flask server
python app.py

# Application will be available at:
# http://localhost:5000
```

### Expose with ngrok
```bash
# In a new terminal
ngrok http 5000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

## GitHub Webhook Configuration

### Setup Instructions:

1. **Navigate to Repository Settings**
   - Go to your GitHub repository
   - Click `Settings` → `Webhooks` → `Add webhook`

2. **Configure Webhook**
   ```
   Payload URL: https://your-ngrok-url.ngrok.io/webhook
   Content type: application/json
   Secret: (your webhook secret from .env)
   Events: Push  Pull requests
   Active: Yes
   ```

3. **Test the Integration**
   - Make a commit and push
   - Create a pull request  
   - Merge a pull request
   - Watch events appear in real-time

## API Reference

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Web dashboard | HTML page |
| `/webhook` | POST | GitHub webhook receiver | JSON status |
| `/api/events` | GET | Retrieve all events | JSON array |
| `/health` | GET | Health check | JSON status |

### Example API Response:
```json
{
  "status": "success",
  "events": [
    {
      "_id": "60f1b2c3d4e5f6789abc123",
      "request_id": "abc1234",
      "author": "john.doe",
      "action": "PUSH",
      "from_branch": "",
      "to_branch": "main",
      "timestamp": "2025-07-02T04:02:30Z"
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

## Environment Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/` | Yes |
| `DATABASE_NAME` | Database name | `github_webhook_db` | Yes |
| `COLLECTION_NAME` | Collection name | `github_events` | Yes |
| `WEBHOOK_SECRET` | GitHub webhook secret | `your-webhook-secret-key` | Optional |
| `PORT` | Flask server port | `5000` | No |
| `DEBUG` | Enable debug mode | `False` | No |

## Troubleshooting

<details>
<summary><strong>MongoDB Connection Issues</strong></summary>

**Problem**: `Failed to connect to MongoDB`

**Solutions**:
- Ensure MongoDB is running: `mongod --version`
- Check your `MONGO_URI` in `.env` file
- For MongoDB Atlas: Use full connection string with credentials
- For local MongoDB: Ensure service is started
</details>

<details>
<summary><strong>Webhook Not Receiving Events</strong></summary>

**Problem**: GitHub webhook returns 404 or timeout

**Solutions**:
- Verify ngrok is running: `ngrok http 5000`
- Check webhook URL includes `/webhook` endpoint
- Ensure Flask app is running on port 5000
- Check GitHub webhook delivery logs
- Verify payload URL format: `https://xxxxx.ngrok.io/webhook`
</details>

<details>
<summary><strong>UI Not Updating</strong></summary>

**Problem**: Dashboard shows old data

**Solutions**:
- Check browser console for JavaScript errors
- Verify `/api/events` endpoint responds: `curl http://localhost:5000/api/events`
- Clear browser cache and reload
- Check MongoDB connection status
</details>

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

## Features

- **GitHub Webhook Integration** - Full implementation
- **MongoDB Data Storage** - Proper schema and persistence  
- **Real-time UI Updates** - 15-second auto-refresh
- **Event Format Compliance** - Exact specification matching
- **Professional Code Quality** - Clean, documented, error-handled
- **Merge Events** - Merge event handling support
- **Modern Web Interface** - Responsive, beautiful design
- **Security Implementation** - Webhook signature verification

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

## Contributing

For questions or improvements:

1. **Issues**: Report bugs or feature requests
2. **Pull Requests**: Improvements welcome
3. **Contact**: Technical queries

## License

This project is created for personal use and educational purposes.

---

<div align="center">

**GitHub Webhook Receiver**

*Demonstrating full-stack development, real-time web applications, and professional software engineering practices*

![Made with Python](https://img.shields.io/badge/Built%20with-Python-blue.svg)

</div>
