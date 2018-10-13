# Clone The Repository
```shell
git clone https://github.com/fossbalaji/crawler.git
```
## Enter into the working directory

```shell
cd crawlersystem
```
## Install the requirements
```shell
virtualenv venv
. venv/bin/activate
pip intsall -r requirements.txt
```

## Mysql is needed for this project to run
```shell
sudo apt-get install mysql-server
```

# Note: Change Enviroment variables to your mysql user name and password in `envsetup.sh` script

## Run the envsetup file by
```shell
sh envsetup.sh
```

## Create database on mysql

```shell
mysql -u yourusername -p
create database crawler
```

## Finally migrate and run the server
```shell
python manage.py migrate
python manage.py runserver
```

## Open this on your browser
http://127.0.0.1:8000