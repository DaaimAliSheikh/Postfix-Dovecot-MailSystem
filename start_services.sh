#!/usr/bin/bash 

CONTAINER_ID='1597f0d6259c'

docker start "$CONTAINER_ID"
docker exec "$CONTAINER_ID" bash -c "postfix start"
docker exec "$CONTAINER_ID" bash -c "/usr/sbin/dovecot -c /etc/dovecot/dovecot.conf"
