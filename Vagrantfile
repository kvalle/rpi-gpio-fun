# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "raspi-dev"

  config.vm.provision "shell", inline: <<-SCRIPT
    apt-get update
    
    apt-get install python-pip -y
    apt-get install python-dev -y
    pip install RPi.GPIO
    pip install python-dateutil

    apt-get install git -y
    pip install PyYAML
    git clone https://github.com/kvalle/dotfiles.git
    chown -R vagrant dotfiles
SCRIPT

  config.vm.provider "virtualbox" do |vb|
    vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 10000 ]
  end

  config.vm.network "forwarded_port", guest: 1337, host: 1337
  config.vm.synced_folder "", "/home/vagrant/dev"
end
