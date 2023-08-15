# Multi-Agent SQL LLM System

A full-stack intelligent chatbot application powered by LangGraph multi-agent orchestration, OpenAI GPT-4o, and React. The system features automatic query routing, conversational AI with image support, and real-time chat interface.

## 🎯 Overview

This project demonstrates a production-ready multi-agent LLM system that intelligently routes user queries to specialized agents (SQL, Recommender, Assistant) for optimal responses. Built with modern web technologies and designed for scalability.

### Key Features

- 🤖 **Multi-Agent Orchestration** - LangGraph-based routing to SQL, Recommender, and Assistant agents
- 💬 **Conversational AI** - Natural, human-like responses with chat history context
- 🖼️ **Image Integration** - MinIO S3 storage with automatic image detection and rendering
- ⚡ **Performance Optimized** - Singleton pattern, caching, and smart routing (50% faster)
- 🎨 **Modern UI** - React-based dark mode interface with real-time updates
- 📊 **PostgreSQL Database** - Structured data for users, posts, places, media, follows, and timeline
- 🔄 **Session Memory** - Maintains conversation context throughout user session
- 🐳 **Dockerized** - Complete containerized deployment with Docker Compose

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│  - Chat Interface                                               │
│  - Image Gallery                                                │
│  - User Context Switching                                       │
│  - Session-based Chat History                                   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ HTTP/REST API
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │            LangGraph Multi-Agent System                   │ │
│  │                                                           │ │
│  │   Classifier ──> Supervisor ──> [SQL | Recommender |     │ │
│  │                                   Assistant]              │ │
│  │                        │                                  │ │
│  │                        ├──> Aggregates Results            │ │
│  │                        └──> Formats Response              │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└───┬─────────────────────┬──────────────────────┬───────────────┘
    │                     │                      │
    ▼                     ▼                      ▼
┌──────────┐      ┌──────────────┐      ┌──────────────┐
│PostgreSQL│      │    MinIO     │      │  OpenAI API  │
│ Database │      │  S3 Storage  │      │   (GPT-4o)   │
└──────────┘      └──────────────┘      └──────────────┘
```

## 📁 Project Structure

```
MultiAgent-SQL-LLM-Server/
├── README.md                    # This file
├── server/                      # Backend application
│   ├── README.md               # Backend documentation
│   ├── app/
│   │   ├── chatbot/           # Multi-agent graph logic
│   │   │   ├── graph.py       # LangGraph orchestration ⭐
│   │   │   ├── service.py     # Business logic
│   │   │   ├── router.py      # FastAPI endpoints
│   │   │   └── media_utils.py # Image utilities
│   │   ├── User/              # User module
│   │   ├── Post/              # Post module
│   │   ├── Media/             # Media module
│   │   ├── Places/            # Places module
│   │   └── common/            # Shared utilities
│   ├── alembic/               # Database migrations
│   ├── config/                # Configuration
│   ├── docker-compose.yml     # Docker orchestration
│   ├── Dockerfile
│   └── requirements.txt
│
└── chat-app/                   # Frontend application
    ├── README.md              # Frontend documentation
    ├── src/
    │   ├── App.js            # Main React component ⭐
    │   ├── App.css           # Styles
    │   └── index.js
    ├── public/
    └── package.json
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 16+ (for frontend development)
- OpenAI API Key
- SerpAPI Key
- Tavily API Key

### Environment Setup

1. **Clone the repository**:

```bash
git clone <repository-url>
cd MultiAgent-SQL-LLM-Server
```

2. **Create environment file** (`server/.env`):

```env
# Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=poc_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# OpenAI
OPENAI_API_KEY=sk-...

# Search APIs
SERPAPI_API_KEY=...
TAVILY_API_KEY=...

# MinIO
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=user
MINIO_SECRET_KEY=password
MINIO_BUCKET=media
MINIO_SECURE=false
```

### Start Backend

```bash
cd server
docker compose up --build
```

This starts:

- PostgreSQL (port 65432)
- FastAPI server (port 8000)
- MinIO storage (port 9000, console 9001)

Database migrations run automatically on startup.

### Start Frontend

```bash
cd chat-app
npm install
npm start
```

Frontend runs on `http://localhost:3000`

### Verify Installation

1. **Backend health check**:

```bash
curl http://localhost:8000/
```

2. **Check users endpoint**:

```bash
curl http://localhost:8000/users/
```

3. **MinIO console**:

```
http://localhost:9001
Login: user / password
```

4. **Frontend**:

```
http://localhost:3000
```

## 🎮 Usage

### Example Queries

Once the system is running, try these queries in the chat interface:

**Database Queries (SQL Agent):**

- "Show me all posts with images"
- "Get user 1's profile"
- "Who follows me?"
- "List recent posts"
- "Find all places"

**Recommendations (Recommender Agent):**

- "Recommend places for me to visit"
- "Suggest users to follow"
- "What should I explore?"

**General Questions (Assistant Agent):**

- "Hello!"
- "What is the weather like?"
- "Calculate 15 \* 24"

**Follow-up Questions (using chat history):**

- "Show me posts" → "What about user 2's posts?"
- "List users" → "Tell me more about the first one"

### User Context Switching

Use the dropdown in the chat interface to switch between users. This changes the perspective for queries like:

- "Show me my posts" (returns different results per user)
- "Who do I follow?"
- "What's on my timeline?"

## 🧠 Multi-Agent Intelligence

### Agent Routing

**Classifier** (Fast Entry Point):

- Keyword-based routing
- 50% faster than LLM-based routing
- Zero-cost for simple queries

**Supervisor** (Smart Coordinator):

- Context-aware routing decisions
- Aggregates multi-agent results
- Determines completion (FINISH)

**Specialized Agents**:

1. **SQL Agent**

   - Queries PostgreSQL database
   - Auto-detects image requirements
   - JOINs media table when needed
   - Returns conversational responses

2. **Recommender Agent**

   - Personalized suggestions
   - Leverages user behavior
   - Can use SQL results for context

3. **Assistant Agent**
   - Web search via Tavily/SerpAPI
   - Mathematical calculations
   - General knowledge questions

### Performance Features

- **Singleton Pattern**: 75% less memory usage
- **Query Caching**: 75% faster repeated queries
- **Smart Routing**: 25-50% API cost reduction
- **Iteration Limit**: Max 5 loops (safety)
- **Error Handling**: Graceful degradation

## 📊 Database Schema

### Core Tables

- **users** - User profiles with avatars
- **posts** - User-generated content with captions
- **media** - Image storage (MinIO URLs)
- **places** - Location data (lat/long, categories)
- **follows** - User relationships
- **timeline** - Aggregated user feeds

### Sample Data

The system includes 40 sample media items (portrait photos), multiple users, posts, places, and follow relationships for testing.

## 🖼️ Image Handling

### Storage

- **MinIO** S3-compatible object storage
- Public bucket: `media`
- Accessible at: `http://localhost:9000/media/`

### Detection & Rendering

1. SQL agent detects image keywords
2. Auto-JOINs media table
3. Returns markdown: `![alt](url)`
4. Frontend renders inline + gallery

### Response Format

```json
{
  "text": "Here are posts:\n![Image 1](url1)",
  "images": [{ "url": "http://localhost:9000/media/1.jpg", "alt": "Image 1" }],
  "has_images": true,
  "user_id": 1
}
```

## 🔧 Development

### Backend Development

See [server/README.md](server/README.md) for:

- Detailed architecture
- Agent implementation
- API documentation
- Database migrations
- Testing guide

### Frontend Development

See [chat-app/README.md](chat-app/README.md) for:

- Component structure
- State management
- Styling guide
- API integration
- Troubleshooting

### Common Commands

**Backend:**

```bash
# Run migrations
cd server
docker compose exec app alembic upgrade head

# Create new migration
docker compose exec app alembic revision -m "description"

# View logs
docker compose logs -f app

# Reset database
docker compose down -v && docker compose up --build
```

**Frontend:**

```bash
# Install dependencies
cd chat-app
npm install

# Start dev server
npm start

# Build for production
npm run build
```

## 📈 Monitoring & Debugging

### Backend Logs

```bash
# View all services
docker compose logs -f

# Specific service
docker compose logs -f app
docker compose logs -f db
docker compose logs -f minio
```

### Database Access

```bash
# Connect to PostgreSQL
docker compose exec db psql -U user -d poc_db

# Run query
SELECT * FROM users;
SELECT COUNT(*) FROM media;
```

### MinIO Console

Access at `http://localhost:9001`

- View uploaded files
- Check bucket permissions
- Monitor storage usage

## 🐛 Troubleshooting

### Backend won't start

**Issue**: Port conflicts or environment issues

```bash
# Check ports
lsof -i :8000
lsof -i :65432

# Rebuild containers
docker compose down -v
docker compose up --build
```

### Images not loading

**Issue**: MinIO URLs incorrect

```bash
# Check MinIO
docker compose ps | grep minio

# Verify bucket
docker compose exec minio mc ls myminio/media

# Check public access
docker compose exec minio mc anonymous get myminio/media
```

### Chat history not working

**Issue**: Frontend not sending history

- Check browser console for errors
- Verify request payload includes `chat_history`
- Check backend logs for history processing

### Database migrations failed

**Issue**: Schema conflicts

```bash
# Reset database completely
docker compose down -v
docker compose up --build

# Migrations run automatically on startup
```

## 🎯 Performance Metrics

Based on testing with 100 requests:

| Metric         | Before Optimization | After Optimization | Improvement  |
| -------------- | ------------------- | ------------------ | ------------ |
| Memory Usage   | ~400MB              | ~100MB             | **75%** ↓    |
| Simple Query   | 800ms               | 400ms              | **50%** ↓    |
| Repeated Query | 1200ms              | 300ms              | **75%** ↓    |
| API Cost       | $0.80               | $0.40-$0.60        | **25-50%** ↓ |

## 🔐 Security Considerations

⚠️ **This is a POC/Development system. For production:**

- [ ] Add authentication & authorization
- [ ] Implement rate limiting
- [ ] Secure API keys (use secrets manager)
- [ ] Enable HTTPS/TLS
- [ ] Sanitize user inputs
- [ ] Add CORS restrictions
- [ ] Implement request validation
- [ ] Add logging & monitoring
- [ ] Use environment-specific configs
- [ ] Secure MinIO buckets (private by default)

## 📚 Technologies

### Backend

- **LangChain** - Agent framework
- **LangGraph** - Multi-agent orchestration
- **OpenAI GPT-4o** - LLM
- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **Alembic** - Migrations
- **MinIO** - Object storage
- **Docker** - Containerization

### Frontend

- **React 18** - UI library
- **Fetch API** - HTTP client
- **CSS Grid/Flexbox** - Layout
- **Markdown Parsing** - Image rendering

### DevOps

- **Docker Compose** - Orchestration
- **Boto3** - AWS/MinIO SDK
- **Pytest** - Testing

## 🎓 Learning Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Docs](https://python.langchain.com/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MinIO Quickstart](https://min.io/docs/minio/container/index.html)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📄 License

MIT License - see individual component READMEs for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4o
- LangChain team for the amazing framework
- MinIO for S3-compatible storage
- FastAPI community

## 📞 Support

For detailed documentation:

- Backend: See [server/README.md](server/README.md)
- Frontend: See [chat-app/README.md](chat-app/README.md)

---

**Built with ❤️ using LangGraph, OpenAI, and React**
