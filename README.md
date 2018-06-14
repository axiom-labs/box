# Axiom Box
A Raspberry Pi voice kit. This initial version utilizes the Voice Bonnet provided by the Google AIY Voice Kit, 2.0.

## Installing Dependencies
First, clone the package to your Pi's home directory under a directory named "axiom":

```
sudo apt-get install git
cd ~
git clone git@github.com:axiom-labs/box.git axiom
```

## Configure
```
cd ~/axiom
sudo setup/install_deps.sh
sudo setup/install_drivers.sh
sudo setup/install_services.sh
```

## Reboot
```
sudo reboot
```
