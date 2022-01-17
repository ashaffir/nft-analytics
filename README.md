# NFT-Analytics
Tracking NFT collections and assets for further analysis

## Setup
Install RabbitMQ server

### Linux: 
sudo apt install rabbitmq-server
sudo service rabbitmq-server start

### Server
* Make sure to use Python 3.8 or higher

ptyhon -m venv venv
source ./venv/bin/activate

pip install -r requirements.txt
python manage.py migrate

### Run server locally
./manage runserver

Open the browser on: http://localhost:8000

### Run Celery
<!-- Start Celery worker -->
celery -A tony_proj worker -l INFO

<!-- Start CElry Beat to send tasks to the workers -->
celery -A tony_proj beat -l INFO  --scheduler django_celery_beat.schedulers:DatabaseScheduler

## Notes
* The database was save to git, so that there will be demo data (graphs)