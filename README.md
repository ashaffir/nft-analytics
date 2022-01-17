# NFT-Analytics
Tracking NFT collections and assets for further analysis

## Setup
Install RabbitMQ server

### Linux: 
sudo apt install rabbitmq-server
sudo service rabbitmq-server start

### Server
* Make sure to use Python 3.8 or higher

python3 -m venv venv
source ./venv/bin/activate

pip install -r requirements.txt
<!-- You can ignore the error that appears in this stage -->

### Run server locally
python3 ./manage.py runserver

Open the browser on: http://localhost:8000

### If you like to activate the periodic tasks that save collections information:
1- Open another termina window
2- Go to the project directory
3- Run:
<!-- Start Celery worker -->
celery -A tony_proj worker -l INFO

4- Open another termial window
5- Go to the project directory
6- Run
<!-- Start CElry Beat to send tasks to the workers -->
celery -A tony_proj beat -l INFO  --scheduler django_celery_beat.schedulers:DatabaseScheduler

At the moment, the task manager will save every minute. For testing and debut purposes. 
This can be defined in the super-admin area.

## Notes
* The database was save to git, so that there will be demo data (graphs)
* Access the super-admin area (Database view) with the following credentials:
username: tony
password: Nft2022!