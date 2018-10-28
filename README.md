# Axiom Box
A Raspberry Pi voice kit. This initial version utilizes the Voice Bonnet provided by the Google AIY Voice Kit, 2.0.

## Installing Dependencies
First, clone the package to your Pi's home directory under a directory named "axiom":

```
sudo apt-get install git
cd ~
git clone git@github.com:axiom-labs/box.git axiom
```

The following instructions will depend on your hardware setup.

## AIY
```
cd ~/axiom
sudo aiy/setup/install_deps.sh
sudo aiy/setup/install_drivers.sh
sudo aiy/setup/install_services.sh
```

## Matrix Creator
```
cd ~/axiom
sudo matrix_creator/setup/install_deps.sh
```

## Reboot
```
sudo reboot
```
