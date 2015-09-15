sudo apt-get install -y python-pip python-dev libxml2-dev libxslt-dev zlib1g-dev python-psycopg2 postgresql \
    postgresql-contrib
pushd /vagrant
sudo pip install -r requirements.txt
sudo python manage.py runserver 0.0.0.0:80 &

