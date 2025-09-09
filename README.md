# Yandex to Google Calendar Sync

Приложение на Python для автоматической синхронизации событий из Яндекс.Календаря в Google Calendar. Поддерживает Docker для развертывания на сервере с непрерывной работой.

## Возможности

- ✅ Синхронизация всех событий из Яндекс.Календаря в Google Calendar
- ✅ Поддержка повторяющихся событий и событий на весь день
- ✅ Автоматическое обновление измененных событий
- ✅ Отслеживание состояния синхронизации для избежания дублирования
- ✅ Docker поддержка для развертывания на сервере
- ✅ Настраиваемые интервалы синхронизации
- ✅ Подробное логирование
- ✅ Автоматический перезапуск при ошибках

## Требования

- Python 3.11+
- Аккаунт Яндекс с доступом к календарю
- Google аккаунт с доступом к Calendar API
- Docker (для развертывания в контейнере)

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/Sirnilin/yandex-to-google-calendar.git
cd yandex-to-google-calendar
```

### 2. Настройка Яндекс.Календаря

1. Включите двухфакторную аутентификацию в Яндекс аккаунте
2. Создайте пароль приложения:
   - Перейдите в [Настройки безопасности](https://passport.yandex.ru/profile/security)
   - Найдите раздел "Пароли приложений"
   - Создайте новый пароль для приложения "Календарь"
   - Сохраните сгенерированный пароль

### 3. Настройка Google Calendar API

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google Calendar API:
   - Перейдите в "APIs & Services" > "Library"
   - Найдите "Google Calendar API" и включите его
4. Создайте OAuth 2.0 credentials:
   - Перейдите в "APIs & Services" > "Credentials"
   - Нажмите "Create Credentials" > "OAuth client ID"
   - Выберите "Desktop application"
   - Скачайте JSON файл и сохраните как `data/credentials.json`

### 4. Настройка окружения

```bash
# Создайте директории для данных
mkdir -p data logs

# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env файл с вашими данными
nano .env
```

Заполните `.env` файл:

```env
YANDEX_USERNAME=your_email@yandex.ru
YANDEX_PASSWORD=your_app_password_from_step_2
GOOGLE_CALENDAR_ID=primary
SYNC_INTERVAL_MINUTES=30
```

### 5. Запуск с Docker (рекомендуется)

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 6. Запуск без Docker

```bash
# Установка зависимостей
pip install -r requirements.txt

# Разовая синхронизация
python main.py once

# Непрерывная синхронизация
python main.py continuous
```

## Настройка

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `YANDEX_USERNAME` | Email Яндекс аккаунта | **Обязательно** |
| `YANDEX_PASSWORD` | Пароль приложения Яндекс | **Обязательно** |
| `YANDEX_CALDAV_URL` | URL CalDAV сервера Яндекс | `https://caldav.yandex.ru` |
| `GOOGLE_CALENDAR_ID` | ID Google календаря | `primary` |
| `SYNC_INTERVAL_MINUTES` | Интервал синхронизации в минутах | `30` |
| `DAYS_AHEAD` | Количество дней вперед для синхронизации | `30` |
| `DAYS_BEHIND` | Количество дней назад для синхронизации | `7` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |

### Google Calendar ID

Чтобы найти ID календаря Google:

1. Откройте [Google Calendar](https://calendar.google.com/)
2. Найдите нужный календарь в списке слева
3. Нажмите на три точки рядом с календарем > "Settings and sharing"
4. Прокрутите вниз до "Calendar ID"
5. Скопируйте ID (например: `your_email@gmail.com` или случайная строка)

## Использование

### Режимы работы

```bash
# Разовая синхронизация
python main.py once

# Непрерывная работа (по расписанию)
python main.py continuous
```

### Мониторинг

Приложение создает подробные логи в файле `sync.log` и выводит информацию в консоль:

```
2024-01-01 12:00:00 - INFO - Starting calendar synchronization
2024-01-01 12:00:01 - INFO - Connected to Yandex Calendar
2024-01-01 12:00:02 - INFO - Found 5 events in Yandex Calendar
2024-01-01 12:00:03 - INFO - Created event: Meeting with team
2024-01-01 12:00:04 - INFO - Sync completed: 3 new, 2 updated, 0 errors
```

### Состояние синхронизации

Приложение сохраняет состояние в `data/sync_state.json` для отслеживания уже синхронизированных событий и избежания дублирования.

## Развертывание на сервере

### Использование Docker Compose

1. Клонируйте репозиторий на сервер
2. Настройте `.env` файл
3. Поместите `credentials.json` в папку `data/`
4. Запустите:

```bash
docker-compose up -d
```

### Автоматический перезапуск

Docker Compose настроен на автоматический перезапуск контейнера при ошибках или перезагрузке сервера:

```yaml
restart: unless-stopped
```

### Мониторинг здоровья

Контейнер включает health check для мониторинга состояния:

```bash
# Проверка статуса
docker-compose ps

# Просмотр health check логов
docker inspect yandex-to-google-calendar
```

## Устранение неполадок

### Ошибки аутентификации Яндекс

- Убедитесь, что используете пароль приложения, а не основной пароль
- Проверьте, что двухфакторная аутентификация включена
- Убедитесь, что email и пароль указаны правильно

### Ошибки Google Calendar API

- Проверьте, что `credentials.json` файл правильно размещен
- Убедитесь, что Calendar API включен в Google Cloud Console
- При первом запуске следуйте инструкциям OAuth авторизации

### Проблемы с Docker

```bash
# Просмотр логов
docker-compose logs -f

# Перезапуск сервиса
docker-compose restart

# Пересборка при изменениях
docker-compose up --build -d
```

### Отладка

Для более подробного логирования установите:

```env
LOG_LEVEL=DEBUG
```

## Лицензия

MIT License

## Поддержка

Если у вас возникли проблемы или вопросы, создайте issue в этом репозитории.