# VKinder - найди свою половинку

VKinder поможет найти свою вторую половинку, основываясь на данных с твоей страницы ВКонтакте, если каких-то данных не достает - бот попросит их ввести

## Комманды

1. "Начать" или "Настройки" - запускает бота, собирает данные пользователя и просит их дополнить, если это необходимо
2. "Дальше" - позволяет вывести следующего подходящего под запрос человека
3. "Стоп" - останавливает поиск людей до следующего запуска командой "Начать"

## Технические подробности

### Библиотеки

Были использованы следующие библиотеки:

1. vk_api - обертка над VK API, позволяющая удобно работать с API ВКонтакте
2. peewee - простая и удобная ORM для работы с базой данных
3. python-dotenv - позволяет загружать переменные окружения из файлов

### Архитектура проекта

1. core - код, использующийся во всем проекте
2. core.utils - утилиты, использующиеся во всем проекте
3. database - код для работы с базой данных (модели, функции для работы с БД)
4. search - код для поискового движка
5. vk - код, относящийся к использованию API ВКонтакте
6. vk.bot - код, реализующий чат-бота (отслеживание событий и реакция на них)
7. vk.tools - код, реализующий работу с общим API ВКонтакте (получение информации о пользователях, фотографиях и т.д.)
8. main.py - точка входа в приложение

## Установка и запуск

### Предварительная подготовка

Для запуска проекта потребуются два токена для API ВКонтакте - токен приложения и токен сообщества.

Токен сообщества позволяет писать сообщения от имени сообщества, а также отслеживать входящие сообщения от других пользователей

Токен приложения позволяет делать все остальное, что не связано напрямую с сообществом - искать пользователей, получать информацию о них и т.д.

#### Получение токена приложения (APPLICATION_TOKEN)

1. Войти в ВК под своим аккаунтом
2. Нажать в левом меню "Управление"
3. Нажать кнопку "Создать" и заполнить форму - ввести любое название и выбрать тип "Standalone-приложение"
4. Нажать кнопку "Подключить приложение"
5. Перейти на вкладку "Настройки" и скопировать "ID приложения"
6. Вставить в адресную строку браузера следующую ссылку, заменив <id приложения> на свое, и перейдя по полученной ссылке:

    ```
    https://oauth.vk.com/authorize?client_id=<id приложения>&display=page&scope=photos,offline&response_type=token&v=5.131
    ```

    Примечание о scope=photos,offline: photos позволяет использовать VK API для доступа к фотографиям пользователей, а offline - позволяет использовать токен бесконечное количество времени

7. После перехода по ссылке необходимо подтвердить свое намерение, после чего ссылка в адресной строке примет следующий вид:

    ```
    https://oauth.vk.com/blank.html#access_token=<токен приложения>&expires_in=0&user_id=<id пользователя>
    ```

    Отсюда необходимо скопировать и сохранить только <токен приложения> (все после "access_token=" и до "&expires_in")

#### Получение токена сообщества (COMMUNITY_TOKEN)

Будем исходить из того, что сообщество уже создано - осталось его настроить и получить токен

1. В сообществе заходим во вкладку "Управление" -> "Работа с API"
2. Нажать кнопку "Создать ключ" и выбрать нужные пункты (для этого проекта требуется только доступ к сообщениям сообщества)
3. Копируем и сохраняем ключ из поля (иногда после второго пункта ключ не создается, тогда повторяем второй пункт)

#### Настройка сообщества

1. В сообществе заходим во вкладку "Управление"
2. Переходим во вкладку "Сообщения" и в выпадающем меню выбираем "Включены"
3. Нажимаем кнопку "Сохранить"
4. Опционально: перейти во вкладку "Возможности для ботов", включить их и добавить кнопку "Начать", также не забываем сохранить изменения

### Загрузка и настройка проекта

0. Необходимо установить Python 3.11 или выше с [официального сайта](https://www.python.org/)
1. Клонировать этот репозиторий
2. Создать файл `./.env` в корневой папке проекта, взяв за основу файл `./.env.template`. Вставить туда полученные токены
3. Настроить константы по пути `./source/core/constants.py`
4. Создать и активировать виртуальное окружение:

    ```
    python -m venv .venv
    .venv/scripts/activate
    ```

5. Установить зависимости из файла `./requirements.txt`:

    ```
    pip install -r requirements.txt
    ```

6. Запустить проект:

    ```
    python ./source/main.py
    ```
