Впринципе достаточно подробное решение описано тут https://serengetitech.com/tech/configuring-angular-jenkins-and-gitlab-for-ci-cd/, но там не учтены сборки с нескольких веток + пайплайны собраны на webинтерфейсе jenkins.

В своём решении я хочу использовать multibranch pipeline, пайплайн будет запускаться для каждой ветки, в которой есть jenkinsfile.

Возможность отката к предыдущему билду обеспечивается за счёт запуска pipeline для каждого push в фича-ветку, то есть можно откатить код на уровне хранилища версий и ветка будет пересобрана и передеплоена. 

На nginx есть один конфиг, который раздаёт все локальные файлы в корневой папке var/www/html, с примерно следующим содержанием, в корневом location раздающий master ветку. В конце он инклудит конфиги других локейшенов, они динамически генерируются во время исполнения jenkins пайплайна по имени ветки.

server {  
    listen 443;
    include    /etc/nginx/SSL.conf;
    server_name test-nginx.example;
    location / {  
        alias /var/www/html/master;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        }
    include /etc/nginx/conf.d/angular_locations/*.conf     
    }


Вопросы, замечания, идеи:
- Вместо одного агента и передачи данных по scp напрямую на тестовый nginx можно было бы попробовать сделать несколько агентов и хранилище артефактов билда например. Тогда после сохранения артефактов в репозитории jenkins мог бы сам подключаться на тестовый nginx (выступает в качестве агента) и задеплоить туда файлы.
- Всё очень сильно сломается если использовать "/" в названии ветки, поэтому нужно либо ограничить нейминг ветки, либо как-то преобразовать / в _ например уже в момент деплоя
- Было бы круто добавить различные проверки и уведомления.