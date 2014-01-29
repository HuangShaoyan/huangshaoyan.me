# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", "1"]
    vb.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.network :forwarded_port, guest: 80, host: 8080

  # use local git repo as saltstack gitfs
  config.vm.define "dev" do |dev|
    dev.vm.hostname = "dev"
    dev.vm.synced_folder "salt/", "/srv/salt/"
  end

  # use github.com as saltstack gitfs
  config.vm.define "test" do |test|
    test.vm.hostname = "test"
    # no additional sync folder needed
  end
end
