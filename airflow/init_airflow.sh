sudo apt-get update
sudo apt-get upgrade -y
sudo apt install -y docker.io docker-compose

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.0/docker-compose.yaml'

mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

docker-compose up airflow-init

docker-compose up -d

sudo usermod -aG docker ubuntu