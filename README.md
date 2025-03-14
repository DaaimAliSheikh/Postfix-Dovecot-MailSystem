Setup docker container with port mapping:
docker run -it --name postfix-smtp -p 25:25 -p 143:143 ubuntu

NOTE: Don't use sudo inside docker, you are already root user

Step 1: Install Postfix and Dovecot
sudo apt update
sudo apt install nano postfix dovecot-core dovecot-imapd
-Choose Internet Site
-System Mail Name, eg: gmail.com
-For rest, choose randomly

Step 2: Configure Postfix
sudo nano /etc/postfix/main.cf

myhostname = gmail.com
myorigin = /etc/mailname
mydestination = $myhostname, localhost.$mydomain, localhost
relayhost =
mynetworks = 127.0.0.0/8
inet_interfaces = all
home_mailbox = Maildir/ # every user will have a Maildir where their mails will be stored

Step 3: Configure Dovecot

sudo nano /etc/dovecot/dovecot.conf
protocols = imap

sudo nano /etc/dovecot/conf.d/10-mail.conf
mail_location = maildir:~/Maildir

sudo nano /etc/dovecot/conf.d/10-auth.conf
disable_plaintext_auth = no # if using docker, then no, otherwise can be yes(plaintext auth not allowed over non secure TLS/SSL connections)
auth_mechanisms = plain login

sudo nano /etc/dovecot/conf.d/10-master.conf
service imap-login {
inet_listener imap {
port = 143
}
}

Step 4: Restart the services to apply configurations
sudo systemctl restart postfix
sudo systemctl restart dovecot

If in docker container:

Initiate services(They don't automatically start on installation/container restart, have to manually start after performing the configurations/restarting):
start postfix: postfix start
start dovecot: /usr/sbin/dovecot -c /etc/dovecot/dovecot.conf

restart services:
restart the container and start the service again

Step 5: Add your users
sudo adduser mailuser

Step 6: Running the frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py

Additional Notes:

- docker ps -a to list containers
- docker start/restart/stop <container_id>
- docker exec -it <container_id> bash to go into container
- docker container rm <container_id>
- postfix/dovecot logs: sudo tail -f /var/log/mail.log
