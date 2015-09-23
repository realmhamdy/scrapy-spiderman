# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty32"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  # an example of sharing the spider folder from your machine to vagrant
  # config.vm.synced_folder "C:/Users/Adri/spiders", "/home/vagrant/myspiders"
  config.vm.provision "shell", path: "setup.sh"
end
