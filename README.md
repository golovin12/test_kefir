Тестовое задание в KEFIR от 02.2022

# Задание:
### 1) Написать сервис для хранения данных о пользователях
При разработке необходимо использовать язык Python. Для работы с БД, реализации веб-сервера и т.д. можно использовать любые библиотеки.
1. Аутентификация в сервисе происходит с помощью cookie.
2. Администраторы могут видеть все данные пользователей и изменять их.
3. Простые пользователи могут видеть лишь ограниченное число данных обо всех пользователях и редактировать часть своих данных.

Спецификация API уже готова. Осталось создать сервис, который реализует этот API.

Так как любой продукт можно сделать лучше, то строгое соответствие API не обязательно, но каждое различие реализации API и спецификации необходимо аргументированно объяснить. 

Так же в представленном API не описаны возможные ошибки и их коды, но было бы неплохо по итогу иметь список возможных ошибок.

Тесты, Swagger, документация, контейнеризация - по желанию, но ведь хорошо, когда всё это есть.

Файл: '[kfr_python_junior_test_openapi.json](kfr_python_junior_test_openapi.json)'

### 2) Примечание
В качестве выполненного задания принимается публичный git репозиторий.

При неплохом знании другого языка, например, go и наличии сильного желания выучить Python, можно выполнить задание на том языке, который уже Вам хорошо знаком.

# Комментарии моего решения:
## Сервис для хранения данных о пользователях
>Модели созданы на основе спецификации API. Из различий: Во все модели добавлено поле login, которое служит для идентификации пользователей.  

>Админы не могут менять поле "id" у пользователей, но могут менять поле "login". 
Это сделано для того, чтобы не нарушалась связь между объектами, если появятся дополнительные связные модели.  

>Также для упрощения поиска пользователей было добавлено 2 фильтра: фильтр сортировки (через параметр ordering) и фильтр поиска (через параметр search).  

>Пользователям была добавлена возможность входить в аккаунт не только по логину, но и по почте (просто дополнительная функция, которая упростит авторизацию пользователей).  

>Для админов была добавлена возможность управлять таблицей городов через patch: private/cities/ и private/cities/{pk}.  

>Также в модель пользователя было добавлено 2 поля: 1) Дата создания - очень полезное поле, чтобы знать когда пользователь был создан. 2) Дата последнего входа - также полезное поле, позволяющее следить за активностью пользователей.
## Используемые библиотеки:
>Django, django-rest-framework, django-filter  

>Также используется библиотека django-debug-toolbar для вывода отладочной панели инструментов  

>Также подключен swagger с использованием библиотеки drf-yasg
## Возможные ошибки:
>404 - когда задан неверный адрес или не вышло получить объект модели  

>403 - когда у пользователя не хватает прав для доступа к странице  

>400 - когда происходит ошибка при валидации полей  

>Не разобрался как вывести ошибку 401 в drf, используя встроенный механизм проверки аутентификации  

>Не понял когда нужно выводить ошибку 422, если при валидации json, то чтобы это реализовать придётся дополнять каждый метод, который работает с валидацией и менять поведение, чтобы выводить нужный код ошибки (не считаю, что это нужно, т.к. информация об ошибка всеравно выводится пользователю).  
## Тесты:
>Тесты написаны только для тестирования базового функционала api.

## Фидбек:
>Схема соблюдена, метаданные о городах есть, пагинация есть. Класс пагинатора имеет неправильную схему ответа, но она не используется (в коде используется корректная).

>Так же присутствует API управления городами, что, несомненно, плюс.
