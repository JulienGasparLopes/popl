Build

```bash
docker build -t flask-app .
```

Start

```bash
docker run -p 5000:5000 flask-app
```


Or with one docker compose command

```bash
docker-compose up -d
```