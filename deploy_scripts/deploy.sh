source ~/.pyenv/versions/quarantine_proj_env/bin/activate
cd /root/quarantined_backend/
git stash
git pull origin master
pip install -r requirements.txt
# remove some pyc files
sudo systemctl stop nginx
sudo systemctl stop gunicorn.socket
find . -name '*.pyc' -delete
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl start gunicorn.socket
sudo systemctl start nginx
echo "Deploy done"
