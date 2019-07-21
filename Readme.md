## In Production
Updating your app
In this scenario, the best way to make changes to your application:

Make changes and test locally
Push the changes to your remote Github repo
Pull the changes from your virtual machine
To pull any changes to you've made to your application, make sure you're in the app parent directory:

```cd ~/app```
Pull the repo with the following command:

```git pull```
Every time you pull any changes from your remote repo, you'll need to restart the app service with:

```sudo systemctl restart app```
If you make any changes to the Nginx sites-enabled file, you'll need to restart Nginx with:

```sudo systemctl restart nginx```
## In Development locally 

https://pythonise.com/feed/flask/deploy-a-flask-app-nginx-uwsgi-virtual-machine
1) To run the server locally: ```uwsgi dev.ini```
1) Once you've had some fun with the application, stop uwsgi with Ctrl + c
2) To kill and quit the wsgi:# ```ps ax|grep uwsgi```
                            # ```kill -s QUIT <pidid>```
3) To kill and reload the uwsgi server:  ```kill `pidof uwsgi` ``` or: ```killall uwsgi```