echo "Instalando Java 8 ..."

sudo add-apt-repository ppa:webupd8team/java

sudo apt update

sudo apt install oracle-java8-installer

javac -version

sudo apt install oracle-java8-set-default

echo "Instalando python3 ... "

sudo apt-get update
sudo apt-get -y upgrade

sudo apt-get install -y python3-pip

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

sudo apt-get install -y python3-venv