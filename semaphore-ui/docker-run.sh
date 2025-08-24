docker run -d \
  --restart unless-stopped \
  --name semaphore \
  -p 3030:3000 \
  --env-file ./.env \
  -e SEMAPHORE_DB_DIALECT=sqlite \
  -v semaphore-data:/var/lib/semaphore \
  -v semaphore-config:/etc/semaphore \
  semaphoreui/semaphore:latest