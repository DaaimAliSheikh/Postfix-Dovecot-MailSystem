# Postfix SMTP & Dovecot Setup in Docker

## Overview
This guide explains how to set up a Docker container running **Postfix SMTP** and **Dovecot** for email services with **port mapping**. The setup includes configuring both services and running a frontend using **Streamlit**.

## Prerequisites
- **Docker** installed on your system
- Basic understanding of Linux and Docker commands

## Step 1: Run the Docker Container
```sh
docker run -it --name postfix-smtp -p 25:25 -p 143:143 ubuntu
```
> **Note:** Inside the Docker container, you are already the root user. Do not use `sudo`.

## Step 2: Install Postfix & Dovecot
```sh
apt update
apt install nano postfix dovecot-core dovecot-imapd
```
### Postfix Configuration Prompts:
- **Choose:** Internet Site
- **System Mail Name:** (e.g., `gmail.com`)
- For the rest, choose randomly.

## Step 3: Configure Postfix
Edit the Postfix main configuration file:
```sh
nano /etc/postfix/main.cf
```
Update the following lines:
```ini
myhostname = gmail.com
myorigin = /etc/mailname
mydestination = $myhostname, localhost.$mydomain, localhost
relayhost =
mynetworks = 127.0.0.0/8
inet_interfaces = all
home_mailbox = Maildir/  # Every user will have a Maildir where their mails will be stored
```

## Step 4: Configure Dovecot
### Update `dovecot.conf`
```sh
nano /etc/dovecot/dovecot.conf
```
Modify:
```ini
protocols = imap
```

### Update `10-mail.conf`
```sh
nano /etc/dovecot/conf.d/10-mail.conf
```
Modify:
```ini
mail_location = maildir:~/Maildir
```

### Update `10-auth.conf`
```sh
nano /etc/dovecot/conf.d/10-auth.conf
```
Modify:
```ini
disable_plaintext_auth = no  # Set to 'no' if using Docker
auth_mechanisms = plain login
```

### Update `10-master.conf`
```sh
nano /etc/dovecot/conf.d/10-master.conf
```
Modify:
```ini
service imap-login {
    inet_listener imap {
        port = 143
    }
}
```

## Step 5: Restart Services
Restart Postfix and Dovecot to apply the configurations:
```sh
systemctl restart postfix
systemctl restart dovecot
```

## Step 6: Start Services in Docker
If running inside a Docker container, use a script to start services:
```sh
bash ./start_services.sh
```
**What this script does:**
- Starts the Docker container specified by the CONTAINER_ID variable inside the script
- Starts Postfix inside the container
- Starts Dovecot inside the container

## Step 7: Running the Frontend
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

## Useful Docker Commands
### List all containers:
```sh
docker ps -a
```
### Start/Restart/Stop a container:
```sh
docker start/restart/stop <container_id>
```
### Access a running container:
```sh
docker exec -it <container_id> bash
```
### Remove a container:
```sh
docker container rm <container_id>
```

## Logs
Check logs for debugging Postfix and Dovecot:
```sh
tail -f /var/log/mail.log
```

---


