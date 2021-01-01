# Deploying Flask API on VM

**STEPS**
## Updating Repositories :
```
sudo apt update
```
## Next, install python and pip :
```
sudo apt install python3-dev python3-pip
```
## Then, run the following command for a wide-system installation of Virtualenv :
```
sudo pip3 install -U virtualenv
```
## Create your first enviroment in a new ./venv directory :
```
virtualenv --system-site-packages -p python3 ./venv
```
## Then, activate the virtual environment to start working inside it. Run the following command:
```
source ./venv/bin/activate
```
## Once you activate venv, move on to installing pip inside the isolated environment :
```
pip install --upgrade pip
```
## Installing Tensorflow :
```
eg .To install TensorFlow for CPU 1.15, run the command:
pip install tensorflow==1.15
```
## Installing NGINX & git
```
sudo apt-get -y install nginx git
sudo apt-get -y install git
```
## Run app
```
export FLASK_APP=application.py
# export FLASK_DEBUG=1 
flask run -h 0.0.0.0
  
OR

nohup python app.py
```
## References
- https://docs.microsoft.com/en-us/azure-stack/user/azure-stack-dev-start-howto-vm-python?view=azs-2008
- https://docs.microsoft.com/en-us/azure-stack/user/azure-stack-dev-start-howto-ssh-public-key?view=azs-2008
- https://docs.microsoft.com/en-us/azure-stack/user/azure-stack-dev-start-howto-deploy-linux?view=azs-2008
- https://phoenixnap.com/kb/how-to-install-tensorflow-ubuntu