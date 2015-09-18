sudo apt-get install -y python-pip python-dev libxml2-dev libxslt-dev zlib1g-dev python-psycopg2 postgresql \
    postgresql-contrib rabbitmq-server python-twisted
pushd /vagrant
sudo pip install -r requirements.txt

if [ ! (-f '/etc/init.d/supervisord')]; then
    sudo curl https://gist.github.com/howthebodyworks/176149/raw/88d0d68c4af22a7474ad1d011659ea2d27e35b8d/supervisord.sh > /etc/init.d/supervisord
    sudo chmod +x /etc/init.d/supervisord
    sudo update-rc.d supervisord defaults
    sudo cp supervisord.conf /etc/
fi
sudo supervisord
