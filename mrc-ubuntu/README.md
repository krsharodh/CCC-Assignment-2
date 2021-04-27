# mrc-ubuntu
MRC instance implememtation demo tailored for Ubuntu, powered by Ansible.

Note:

1.This is the demo for **Ubuntu**. If u want to run it on Windows, please install linux VM or WSL(Windows Subsystem for Linux). If WSL is needed, Please Check [this](https://docs.microsoft.com/en-us/windows/wsl/install-win10 ) for more info.

2.Install ansible and its dependencies before run the script. The commands is shown below:

```
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install ansible
```

3.Run the script `run-nectar.sh` to launch the demo.

If the demo works well, please do Step 4 and 5, to change the acount settings to yours:

4.Please download your openstack rc file from MRC portal and use it to replace openrc.sh.

5.Please create your own key pairs and add the name of the key pairs at the end of "instance_key_name: " (Where can I find it? Check `/host_vars/mrc.yaml`)