# Music App - Deployment & Setup Guide

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- YouTube API Key (optional, for YouTube imports)
- PostgreSQL 15+ (if running locally without Docker)

### Local Development with Docker

1. **Clone and setup:**
```bash
git clone <repo>
cd music-app
cp backend/.env.example backend/.env
```

2. **Configure environment:**
Edit `backend/.env`:
```
DB_HOST=db
DB_PORT=5432
DB_NAME=music_app
DB_USER=postgres
DB_PASSWORD=postgres
YOUTUBE_API_KEY=your_key_here
```

3. **Run with Docker Compose:**
```bash
docker compose up --build
```

4. **Access the app:**
- Frontend: http://localhost:3000
- API: http://localhost:5000
- Database: localhost:5432

### Local Development (Without Docker)

1. **Install PostgreSQL:**
```bash
# macOS
brew install postgresql@15

# Ubuntu
sudo apt-get install postgresql-15

# Windows
# Download from https://www.postgresql.org/download/windows/
```

2. **Create database:**
```bash
createdb music_app
```

3. **Backend setup:**
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your database credentials
npm run dev
```

4. **Frontend setup (new terminal):**
```bash
cd frontend
npm install
npm start
```

## Database Schema

### Songs Table
- `id` (UUID) - Primary key
- `title` (String) - Song title
- `artist` (String) - Artist name
- `album` (String) - Album name
- `duration` (Integer) - Duration in seconds
- `genre` (String) - Genre
- `cover` (Text) - Cover image URL
- `youtubeId` (String) - YouTube video ID
- `source` (Enum) - 'local' or 'youtube'
- `createdAt` (Timestamp)
- `updatedAt` (Timestamp)

### Playlists Table
- `id` (UUID) - Primary key
- `name` (String) - Playlist name
- `description` (Text) - Playlist description
- `createdAt` (Timestamp)
- `updatedAt` (Timestamp)

### PlaylistSongs (Join Table)
- `playlistId` (UUID) - Foreign key to Playlists
- `songId` (UUID) - Foreign key to Songs

## API Endpoints

### Songs
- `GET /api/songs` - Get all songs
- `GET /api/songs/:id` - Get song by ID
- `GET /api/songs/search/:query` - Search songs

### Playlists
- `GET /api/playlists` - Get all playlists
- `POST /api/playlists` - Create playlist
- `POST /api/playlists/:id/songs/:songId` - Add song to playlist
- `DELETE /api/playlists/:id/songs/:songId` - Remove song from playlist

### YouTube Integration
- `POST /api/import/youtube-playlist` - Import YouTube playlist
- `POST /api/import/youtube-channel` - Import channel videos
- `GET /api/search/youtube/:query` - Search YouTube

### Health
- `GET /health` - Health check

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci-cd.yml`) runs:
1. **Backend Tests** - Jest unit tests with coverage
2. **Frontend Build** - React build validation
3. **Security Scan** - Trivy vulnerability scanning
4. **Docker Build** - Build & push to Docker Hub (on main branch)

### Setup GitHub Actions Secrets:
```
DOCKER_USERNAME = your_docker_username
DOCKER_PASSWORD = your_docker_token
```

## YouTube Import Setup

1. **Get API Key:**
   - Go to https://console.cloud.google.com
   - Create new project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 API key

2. **In App:**
   - Click "📥 Import YouTube"
   - Enter API key
   - Paste playlist ID or channel ID
   - Click Import

## Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View backend logs
docker compose logs backend

# Reset database
docker volume rm music_app_postgres_data
docker compose up --build
```

### Port Already in Use
```bash
# Find process using port
lsof -i :3000  # frontend
lsof -i :5000  # backend
lsof -i :5432  # database

# Kill process
kill -9 <PID>
```

### Build Failures
```bash
# Clean rebuild
docker compose down -v
docker compose build --no-cache
docker compose up
```

## Production Deployment

### Using Docker Hub Registry:

1. **Push to registry:**
```bash
docker tag music-app-backend:latest user/music-app-backend:latest
docker push user/music-app-backend:latest
```

2. **Deploy with production compose file:**
Create `docker-compose.prod.yml` with:
- SSL/TLS configuration
- Environment-specific variables
- Resource limits
- Restart policies

3. **Use Kubernetes (optional):**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Performance Optimization

- Frontend: Multi-stage build reduces image from ~500MB to ~150MB
- Backend: Connection pooling with Sequelize
- Database: Indexes on frequently searched columns
- Caching: Use Redis for session management (future)

## Security Best Practices

- Never commit `.env` files
- Use GitHub Secrets for sensitive data
- Enable HTTPS in production
- Validate all user inputs
- Use prepared statements (Sequelize does this)
- Regular security scans with Trivy
