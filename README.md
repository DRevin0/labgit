# LabGit

## Структура проекта

```text
labgit/
├── .github/workflows/ci.yml
├── ansible/
│   ├── inventory.ini
│   └── playbook.yml
├── project/
│   ├── backend/
│   ├── frontend/
│   └── docker-compose.yml
├── .trufflehog-ignore
└── README.md
````

## Архитектура

```text
Ноутбук
   │
   ├── Ansible / SSH ──→ Debian VM
   │                       │
   │                       └── Docker Compose
   │                            ├── frontend / nginx :80
   │                            │       │
   │                            │       └── /api/status
   │                            │
   │                            └── backend / Flask :5000
   │
   └── Браузер ──→ VM:8080 ──→ frontend
```

Frontend опубликован наружу:

```text
192.168.122.157:8080 → frontend:80
```

Backend напрямую наружу не публикуется.

## Запуск через Ansible

На хосте:

```bash
cd ~/Documents/gitfolder/labgit/ansible
```

Проверить подключение к VM:

```bash
ansible -i inventory.ini webservers -m ping
```

Ожидается:

```text
"ping": "pong"
```

Запустить развёртывание:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

Playbook:

* устанавливает необходимые зависимости;
* запускает Docker;
* создаёт `/home/bubba/app`;
* копирует проект на VM;
* запускает Docker Compose.

## Проверка

Проверить контейнеры:

```bash
ssh bubba@192.168.122.157 "docker ps"
```

Должны работать:

```text
lab_frontend
lab_backend
```

Приложение:

```text
http://192.168.122.157:8080
```

Проверить API:

```bash
curl http://192.168.122.157:8080/api/status
```

Backend возвращает JSON:

```json
{
  "status": "online",
  "message": "Привет от бэкенда!",
  "server_time": "YYYY-MM-DD HH:MM:SS"
}
```

`server_time` показывает текущее время сервера.

## Frontend → Backend

Frontend работает через nginx. Запрос:

```text
GET /api/status
```

передаётся на:

```text
backend:5000/api/status
```

То есть:

```text
Браузер
   ↓
frontend / nginx
   ↓
backend:5000
   ↓
Flask /api/status
   ↓
JSON
```

## Docker Compose

Файл:

```text
project/docker-compose.yml
```

запускает два сервиса:

```text
backend  → Flask :5000
frontend → nginx :80
```

Frontend публикуется как `8080:80`, backend наружу не публикуется.

Для ручного запуска непосредственно на VM:

```bash
cd /home/bubba/app
docker compose up -d --build
```

Проверка:

```bash
docker compose ps
```

Остановка:

```bash
docker compose down
```

## GitHub Actions + Trivy

Workflow:

```text
.github/workflows/ci.yml
```

Запускается при `push` и `pull_request` в `main`.

Схема:

```text
git push
   ↓
GitHub Actions
   ↓
Checkout
   ↓
TruffleHog
   ↓
Docker Compose build
   ↓
Trivy → backend
   ↓
Trivy → frontend
```

Проверить результат:

```text
GitHub → Actions → CI Checks
```

## Основные команды

```bash
# Проверить Ansible
cd ~/Documents/gitfolder/labgit/ansible
ansible -i inventory.ini webservers -m ping

# Развернуть приложение
ansible-playbook -i inventory.ini playbook.yml

# Проверить контейнеры
ssh bubba@192.168.122.157 "docker ps"

# Проверить API
curl http://192.168.122.157:8080/api/status

# Проверить Compose
ssh bubba@192.168.122.157 "cd /home/bubba/app && docker compose ps"

# Логи
ssh bubba@192.168.122.157 "docker logs lab_frontend"
ssh bubba@192.168.122.157 "docker logs lab_backend"
```


