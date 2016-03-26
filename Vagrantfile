# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "raspi-dev"

  config.vm.provision "shell", inline: <<-SCRIPT
    echo `whoami`
  sudo apt-get update
    sudo apt-get install python-pip -y
    sudo apt-get install git -y
    sudo pip install PyYAML
    git clone https://github.com/kvalle/dotfiles.git
SCRIPT

  config.vm.provider "virtualbox" do |vb|
    vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 10000 ]
  end

  config.vm.network "forwarded_port", guest: 1337, host: 1337
  config.vm.synced_folder "", "/home/vagrant/dev"
end
