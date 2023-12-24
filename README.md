# Лабораторные работы по предмету "Сетевые технолгии" 4 курс

# 2 лабораторная работа
<h2>Концептуальная модель</h2>
На основе анализа предметной области «Антикварный магазин», были выделены следующие информационные объекты, которые необходимо хранить в базе данных: ЖАНР (genre_id, genre_name), РЕЖИССЕР (director_id, derector_name), СТРАНА (country_id, country_name), КЛИЕНТ (buyer_id, buyer_name), ФИЛЬМ (film_id, genre_id, country_id, year_publication, available_number), АВТОР (author_id, author_name), МЕНЕДЖЕР (manager_id, login, password).
Каждый из выделенных информационных объектов имеет следующие атрибуты:

 - ЖАНР – название жанра; 
 - СТРАНА – название страны; 
 - РЕЖИССЕР – фамилия, имя; 
 - КЛИЕНТ - фамилия, имя, отчество, телефон, адрес; 
 - ФИЛЬМ – название фильма, год премьеры, доступное количество;
 - МЕНЕДЖЕР – логин, пароль;

![ER-диаграмма предметной области "Антикварный магазин"](/2lab/ER_диаграмма_2лаба.png)
<h2>Логическая модель</h2>

![логическая модель ПО "Антикварный магазин"](/2lab/логическая%20модель%20антикварный%20магазин.png)

# 3 лабораторная работа

1. Устанавливаем **ufw**  с помощью команды **sudo  apt  install  ufw**, запускаем его **sudo  ufw  enable**, проверяем запустился ли он с помощью команды **sudo  ufw  status**
![](/3lab/Screenshot_ufw_status.png)
3. Устанавливаем **ssh**, с помощью команды **sudo  apt  install  ssh**, заходим в **sshd_config**. Запрещаем подключения через root-пользователя и разрешаем только созданному нами пользователю.
![](/3lab/Screenshot_sshd_config_2.png)
![](/3lab/Screenshot_sshd_config_3.png)
Заходим в **ssh_config**, меняем стандартный порт на 23.
![](/3lab/Screenshot_ssh_config_1.png)
4. Устанавливаем postgresql (хотя чаще бывает, что postgresql  стоит по умолчанию). Заходим в оболочку postgresql  с помощью команды **sudo -****u** **postgres** **psql**. Создаем базу данных для keycloak и создаем пользователя для управления базой данных. Меняем порт для подключения postgresql
![](/3lab/port_postgers.png)
![](/3lab/Screenshot_postgres_db_list.png)
![](/3lab/Screenshot_keycloak_users.png)
5. Скачиваем zip  архив keycloak с официального сайта, распаковываем его. В папке, где распаковали keycloak создаем текстовый файл dockerfile.
![](/3lab/Screenshot_dockerfile.png)
Собираем docker image, запускаем docker image.
6. Переходим на сайт 127.0.0.1:8080. Теперь создаем своего клиента
![](/3lab/Screenshot_keycloak_client_scopes.png)
![](/3lab/Screenshot_keycloak_clients.png)
Создаем свою группу
![](/3lab/Screenshot_keycloak_groups.png)
Добавляем свою realm-role
![](/3lab/Screenshot_keycloak_realm_roles.png)
Добавляем своего пользователя
![]()
6. Теперь пишем запросы. Используя HTTP-клиент Postman, нужно протестировать отправку запросов на Keycloak.
Необходимые виды запросов:
- Получение токена по паролю POST
- Получение пользователей GET http://localhost:8080/realms/realm/protocol/openid-connect/userinfo
- Получение токена по refresh токену POST http://localhost:8080/realms/test-realm/protocol/openid-connect/token
- Получение информации про реалм GET http://localhost:8080/realms/test-realm/.well-known/uma2-configuration
![](/3lab/Screenshot_1_request.png)
![](/3lab/Screenshot_2_request.png)
![](/3lab/Screenshot_3_request.png)
![](/3lab/Screenshot_4_request.png)
