# API CI/CD Automation Project

Проект автоматизации тестирования API с использованием Pytest, Allure, Requests и Docker для CI/CD.

## Используемые библиотеки

### Основные зависимости (`requirements.txt`)
- **requests==2.31.0** - HTTP-библиотека для выполнения API-запросов
- **pydantic==2.5.0** - Валидация данных и работа с моделями данных
- **python-dotenv==1.0.0** - Загрузка переменных окружения из .env файлов
- **PyYAML==6.0.1** - Парсинг и работа с YAML файлами

### Тестовые зависимости (`requirements-test.txt`)
- **pytest==7.4.3** - Фреймворк для написания и запуска тестов
- **pytest-html==4.0.2** - Генерация HTML отчетов о тестировании
- **pytest-timeout==2.2.0** - Установка таймаутов для тестов
- **pytest-rerunfailures==12.0** - Повторный запуск упавших тестов
- **pytest-ordering==0.6** - Управление порядком выполнения тестов
- **allure-pytest==2.13.2** - Интеграция Allure с pytest для генерации отчетов
- **allure-python-commons==2.13.2** - Общие компоненты Allure для Python
- **Faker==20.1.0** - Генерация тестовых данных
- **jsonschema==4.20.0** - Валидация JSON схем
- **deepdiff==6.7.1** - Сравнение объектов и структур данных

## Структура проекта

```
api_ci_cd_auto/
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                   # Образ Docker для тестов
├── pytest.ini                  # Конфигурация pytest
├── requirements.txt            # Основные зависимости
├── requirements-test.txt       # Тестовые зависимости
├── test.env                    # Переменные окружения для тестов
├── .gitignore                  # Игнорируемые файлы для Git
├── .dockerignore               # Игнорируемые файлы для Docker
├── README.md                   # Документация проекта
│
├── tests/                      # Директория с тестами
│   ├── __init__.py
│   ├── conftest.py            # Фикстуры pytest
│   ├── test_CreateBooking.py  # Тесты для работы с бронированиями
│   │
│   └── utils/                 # Вспомогательные утилиты
│       ├── __init__.py
│       ├── api_client.py      # HTTP клиент для API запросов
│       ├── endpoints.py       # Определение эндпоинтов API
│       ├── models.py          # Pydantic модели данных
│       └── validators.py      # Валидаторы и проверки
│
├── test_data/                  # Тестовые данные
├── reports/                    # Отчеты о тестировании (генерируется)
├── logs/                       # Логи (генерируется)
└── venv/                       # Виртуальное окружение Python (не коммитится)
```

### Описание компонентов

#### `tests/conftest.py`
Содержит фикстуры pytest:
- `base_url` - базовый URL API
- `auth_token` - токен авторизации
- `client` - API клиент без авторизации
- `api_client` - API клиент с авторизацией
- `test_user_data` - данные пользователя для авторизации
- `item_data` - тестовые данные для бронирования
- `create_item` - создание тестового бронирования
- `delete_item` - удаление тестового бронирования

#### `tests/utils/api_client.py`
HTTP клиент для работы с API:
- Класс `ApiClient` - основной клиент для выполнения запросов
- Класс `ApiResponse` - обертка над ответом API
- Поддержка всех HTTP методов (GET, POST, PUT, PATCH, DELETE)
- Управление заголовками и авторизацией

#### `tests/utils/endpoints.py`
Определение эндпоинтов API:
- `TOKEN` - получение токена авторизации
- `BOOKING` - работа с бронированиями

#### `tests/utils/models.py`
Pydantic модели для валидации данных:
- `Booking` - модель бронирования
- `BookingAnswer` - ответ при создании бронирования
- `BookingIds` - модель ID бронирования
- `BookingIdsResponse` - список ID бронирований
- `TokenResponse` - ответ с токеном авторизации

#### `tests/utils/validators.py`
Валидаторы и проверки:
- `ResponseValidator` - валидация JSON схем и сравнение объектов
- `Assert` - вспомогательные методы для проверок в тестах

## Как запустить проект

### Предварительные требования

- Python 3.11 или выше
- Docker и Docker Compose (для запуска в контейнере)
- Git

### Локальный запуск

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd api_ci_cd_auto
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
```

3. **Активируйте виртуальное окружение:**
   - Windows (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   - Windows (CMD):
   ```cmd
   venv\Scripts\activate.bat
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Установите зависимости:**
```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

5. **Настройте переменные окружения:**
   - Скопируйте `test.env` в `.env` или используйте `test.env` напрямую
   - При необходимости отредактируйте значения переменных

6. **Запустите тесты:**
```bash
# Базовый запуск
pytest tests/ -v

# С HTML отчетом
pytest tests/ -v --html=reports/report.html

# С Allure отчетом
pytest tests/ --alluredir=allure-results
allure serve allure-results

# Запуск конкретного теста
pytest tests/test_CreateBooking.py -v

# Запуск с маркерами
pytest tests/ -m smoke -v
pytest tests/ -m api -v
```

### Запуск в Docker

1. **Соберите и запустите контейнер:**
```bash
docker-compose up --build
```

2. **Запуск в фоновом режиме:**
```bash
docker-compose up -d --build
```

3. **Просмотр логов:**
```bash
docker-compose logs -f
```

4. **Остановка контейнера:**
```bash
docker-compose down
```

### Переменные окружения

Основные переменные, которые можно настроить в `test.env` или `.env`:

- `CI_API_URL` / `API_URL` - базовый URL API (по умолчанию: `https://restful-booker.herokuapp.com`)
- `TEST_USERNAME` - имя пользователя для авторизации (по умолчанию: `admin`)
- `TEST_PASSWORD` - пароль для авторизации (по умолчанию: `password123`)
- `ENVIRONMENT` - окружение (test/staging/production)
- `LOG_LEVEL` - уровень логирования (DEBUG/INFO/WARNING/ERROR)
- `REQUEST_TIMEOUT` - таймаут запросов в секундах (по умолчанию: 30)

## Маркеры тестов

Проект использует следующие маркеры pytest (определены в `pytest.ini`):

- `@pytest.mark.smoke` - smoke-тесты
- `@pytest.mark.regression` - регрессионные тесты
- `@pytest.mark.api` - тесты API
- `@pytest.mark.slow` - медленные тесты
- `@pytest.mark.positive` - позитивные тесты
- `@pytest.mark.negative` - негативные тесты
- `@pytest.mark.auth` - тесты авторизации
- `@pytest.mark.flaky` - ненадежные тесты

Пример использования:
```bash
pytest -m "smoke and api" -v
pytest -m "not slow" -v
```

## Генерация отчетов

### HTML отчет
```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Allure отчет
```bash
# Генерация результатов
pytest tests/ --alluredir=allure-results

# Просмотр отчета
allure serve allure-results

# Генерация статического отчета
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## CI/CD

Проект готов для интеграции в CI/CD пайплайны. Docker образ можно использовать в:
- GitHub Actions
- GitLab CI/CD
- Jenkins
- Azure DevOps
- Других CI/CD системах

Пример использования в CI/CD:
```yaml
# Пример для GitHub Actions
- name: Run API Tests
  run: |
    docker-compose up --build
    docker cp api-autotests:/app/reports ./reports
```

## Дополнительная информация

- Все тесты используют Allure для детальной отчетности
- Проект поддерживает параллельный запуск тестов
- Настроена автоматическая очистка тестовых данных после выполнения тестов
- Используется валидация данных через Pydantic модели

## Лицензия

[Укажите лицензию проекта]

## Контакты

[Укажите контактную информацию]
