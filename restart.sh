sudo su -
cd /mysite/fridge-help
ps -ef | grep uwsgi | grep -v grep | awk '{print $2}'|xargs kill -9
nohup uwsgi --http :8000 --module demo.wsgi &