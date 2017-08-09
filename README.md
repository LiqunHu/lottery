#推送需要的依赖包
add-apt-repository ppa:chris-lea/node.js
apt-get update
apt-get install nodejs
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
apt-cache search readline
apt-get install libssl-dev sqlite3 libsqlite3-dev
apt-get install libreadline6 libreadline6-dev
apt-get install mysql-server
apt-get install npm
npm install -g cnpm --registry=http://registry.npm.taobao.org
apt-get install nginx
pyenv install 3.5.2
pyenv global 3.5.2
pip install falcon
pip install cython
pip install --no-binary :all: falcon
pip install gevent gunicorn
pip install pycrypto 
pip install jpush
pip install selenium
pip install sqlalchemy
pip install Pillow
pip install pytesseract
pip install BeautifulSoup4


npm i --registry=https://registry.npm.taobao.org

# mysql 5.5
# my.cnf
# [mysqld]
# character_set_server=utf8  

# init_connect='SET NAMES utf8'  


# curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
# sudo apt-get install -y nodejs
# npm install -g cnpm --registry=http://registry.npm.taobao.org
