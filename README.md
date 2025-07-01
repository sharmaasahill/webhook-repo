# TechStax Assessment - GitHub Webhook Receiver

This Flask application receives GitHub webhook events and displays them in a clean web interface. It automatically captures Push, Pull Request, and Merge events from your GitHub repository and stores them in MongoDB.

## 🚀 Features

- **Real-time GitHub Event Monitoring**: Captures Push, Pull Request, and Merge events
- **MongoDB Integration**: Stores all events with proper schema structure  
- **Live Web Interface**: Auto-refreshes every 15 seconds to show latest activities
- **Modern UI**: Clean, responsive design with real-time status indicators
- **Webhook Security**: Optional signature verification for production use
- **Health Monitoring**: Built-in health check endpoints

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- ngrok (for local webhook testing)
- GitHub repository for testing

## 🛠️ Installation & Setup

### 1. Clone and Setup

```bash
# Clone this repository
git clone https://github.com/sharmaasahill/webhook-repo.git
cd webhook-repo

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. MongoDB Setup

Make sure MongoDB is running on your system:

```bash
# Start MongoDB (if installed locally)
mongod

# Verify MongoDB is running
mongosh --eval "db.runCommand('ping')"
```

### 3. Environment Configuration

```bash
# Copy environment example
cp env.example .env

# Edit .env file with your configuration
# Set your MongoDB URI and webhook secret
```

### 4. Run the Application

```bash
# Start the Flask application
python app.py
```

The application will start on `http://localhost:5000`

### 5. Expose with ngrok (for GitHub webhooks)

```bash
# In a new terminal, expose your local server
ngrok http 5000
```

Copy the ngrok HTTPS URL (e.g., `https://abc123.ngrok.io`)

## 🔗 GitHub Webhook Configuration

### 1. Go to your GitHub repository settings
- Navigate to `Settings` → `Webhooks` → `Add webhook`

### 2. Configure the webhook:
- **Payload URL**: `https://your-ngrok-url.ngrok.io/webhook`
- **Content type**: `application/json`
- **Secret**: Set the same secret as in your `.env` file
- **Events**: Select `Push`, `Pull requests`

### 3. Test the webhook:
- Make a commit and push to your repository
- Create a pull request
- Merge a pull request (for brownie points!)

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/webhook` | POST | GitHub webhook receiver |
| `/api/events` | GET | JSON API for events |
| `/health` | GET | Health check endpoint |

## 🗄️ MongoDB Schema

The application stores events with the following structure:

```javascript
{
  "_id": ObjectId,
  "request_id": "string",    // Git commit hash or PR ID
  "author": "string",        // GitHub username
  "action": "string",        // PUSH, PULL_REQUEST, or MERGE
  "from_branch": "string",   // Source branch (empty for push)
  "to_branch": "string",     // Target branch
  "timestamp": "string"      // ISO datetime string
}
```

## 🎨 Event Display Formats

The UI displays events in the following formats:

- **Push**: `{author} pushed to {to_branch} on {timestamp}`
- **Pull Request**: `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **Merge**: `{author} merged branch {from_branch} to {to_branch} on {timestamp}`

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/` |
| `DATABASE_NAME` | Database name | `techstax_assessment` |
| `COLLECTION_NAME` | Collection name | `github_events` |
| `WEBHOOK_SECRET` | GitHub webhook secret | `your-webhook-secret-key` |
| `PORT` | Flask server port | `5000` |
| `DEBUG` | Enable debug mode | `False` |

## 🚨 Troubleshooting

### Common Issues:

1. **MongoDB Connection Error**:
   - Ensure MongoDB is running: `mongod --version`
   - Check your `MONGO_URI` in `.env`

2. **Webhook Not Receiving Events**:
   - Verify ngrok is running and URL is correct
   - Check GitHub webhook delivery status
   - Ensure webhook secret matches

3. **UI Not Updating**:
   - Check browser console for errors
   - Verify `/api/events` endpoint is accessible
   - Check MongoDB connection

### Logs:
The application provides detailed logging. Check the console output for debug information.

## 🧪 Testing

### Manual Testing:
1. Visit `http://localhost:5000` to see the web interface
2. Check `http://localhost:5000/health` for system status
3. Test API endpoint: `http://localhost:5000/api/events`

### GitHub Integration Testing:
1. Make commits to your action-repo
2. Create and merge pull requests
3. Watch events appear in real-time on the web interface

## 📝 License

This project is created for the TechStax assessment and is intended for educational purposes.

## 🤝 Support

For questions regarding this assessment, please refer to the original task documentation or contact the TechStax team.

---

**Note**: This application was developed as part of a technical assessment for TechStax. It demonstrates webhook integration, real-time data processing, and modern web interface design. 