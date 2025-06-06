# BotControlWebSite

**BotControlWebSite** — это веб-приложение для управления ботами через веб-интерфейс. Проект разработан с использованием Python и TypeScript и предоставляет удобный интерфейс для мониторинга и управления ботами.

## 📦 Стек технологий

* **Backend**: Python
* **Frontend**: TypeScript
* **Базы данных**: PostgreSQL, MongoDB
* **Контейнеризация**: Docker, Docker Compose

## 📁 Структура проекта

* `src/` — исходный код приложения
* `docker-compose.yaml` — конфигурация Docker Compose для запуска сервисов
* `postgres.conf` — конфигурационный файл для PostgreSQL
* `mongod.conf` — конфигурационный файл для MongoDB
* `.gitignore` — список файлов и папок, игнорируемых Git

## 🚀 Быстрый старт

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Ncesam/BotControlWebSite.git
   cd BotControlWebSite
   ```

2. **Запустите приложение с помощью Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Это развернет все необходимые сервисы, включая базы данных и веб-интерфейс.

## 🛠️ Конфигурация

* **PostgreSQL**: настройки находятся в `postgres.conf`
* **MongoDB**: настройки находятся в `mongod.conf`

При необходимости вы можете изменить эти файлы для настройки параметров баз данных под свои нужды.
