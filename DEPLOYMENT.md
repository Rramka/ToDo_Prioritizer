# Deployment Guide - ToDo Prioritizer

## Docker Deployment

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- OpenAI API Key

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ToDo_Prioritizer
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Build and start services:**
   ```bash
   docker-compose up -d --build
   ```

4. **Check status:**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (with defaults)
OPENAI_MODEL=gpt-4o-mini
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

### Docker Commands

**Start services:**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f [service-name]
```

**Rebuild after code changes:**
```bash
docker-compose up -d --build
```

**Restart a service:**
```bash
docker-compose restart [service-name]
```

**Check service health:**
```bash
docker-compose ps
```

### Production Deployment

#### 1. Update Environment Variables

For production, update `.env`:
```env
FRONTEND_URL=https://your-domain.com
BACKEND_URL=https://api.your-domain.com
```

#### 2. Security Considerations

- Remove volume mounts in production (read-only volumes are set)
- Use secrets management (Docker secrets, AWS Secrets Manager, etc.)
- Enable HTTPS with reverse proxy (nginx, Traefik)
- Set up proper firewall rules
- Use non-root users (already configured in Dockerfiles)

#### 3. Reverse Proxy Setup (Nginx Example)

```nginx
# Frontend
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Backend API
server {
    listen 80;
    server_name api.your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 4. Docker Compose Production Override

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  backend:
    volumes: []  # Remove development volumes
    environment:
      - FRONTEND_URL=https://your-domain.com
  
  frontend:
    environment:
      - NEXT_PUBLIC_BACKEND_URL=https://api.your-domain.com
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Health Checks

Both services include health checks:
- Backend: `/health` endpoint
- Frontend: HTTP 200 on root

Check health:
```bash
docker-compose ps
# Should show "healthy" status
```

### Troubleshooting

**Services won't start:**
```bash
docker-compose logs
# Check for errors in logs
```

**Port already in use:**
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "3001:3000"  # Frontend
```

**Build failures:**
```bash
docker-compose build --no-cache
```

**Permission issues:**
```bash
# Ensure Docker has proper permissions
sudo usermod -aG docker $USER
```

### Scaling

To scale services:
```bash
docker-compose up -d --scale backend=2
```

Note: Frontend is stateless and can be scaled. Backend is stateless and can be scaled behind a load balancer.

### Monitoring

**View resource usage:**
```bash
docker stats
```

**View service logs:**
```bash
docker-compose logs -f --tail=100
```

### Backup and Recovery

**Backup:**
```bash
# Export environment variables
docker-compose config > docker-compose.backup.yml
```

**Recovery:**
```bash
# Restore from backup
docker-compose -f docker-compose.backup.yml up -d
```

## Cloud Deployment Options

### AWS (ECS/Fargate)
- Use ECS task definitions
- Store secrets in AWS Secrets Manager
- Use Application Load Balancer

### Google Cloud (Cloud Run)
- Deploy as Cloud Run services
- Use Secret Manager for API keys
- Enable Cloud CDN for frontend

### Azure (Container Instances)
- Deploy as Azure Container Instances
- Use Key Vault for secrets
- Use Azure Front Door for CDN

### DigitalOcean (App Platform)
- Deploy directly from GitHub
- Auto-configure environment variables
- Built-in SSL certificates

## Maintenance

**Update dependencies:**
```bash
# Backend
cd backend
pip list --outdated
pip install --upgrade <package>

# Frontend
cd frontend
npm outdated
npm update
```

**Rebuild after updates:**
```bash
docker-compose up -d --build
```

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Verify environment variables
3. Check health endpoints
4. Review Docker documentation

