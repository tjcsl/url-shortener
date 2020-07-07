Vagrant.configure("2") do |config|

  config.vm.box = "generic/ubuntu2004"

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.ssh.forward_agent = true
  config.vm.hostname = "shortenervm"
  config.vm.boot_timeout = 600
  config.vm.define "shortener-vagrant" do |v|
  end

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
    vb.name = "shortener-vagrant"
    vb.memory = 2048 # the default of 512 gives us a OOM during setup.
  end

  config.vm.synced_folder ".", "/home/vagrant/url-shortener"

  config.vm.provision "shell", path: "config/vagrant/provision_vagrant.sh"
  config.ssh.username = "vagrant"

end