#!/bin/bash
USERNAME=foliva
PASSWD=`cat altair.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:SecretpASSword`

REMOTE=altair.dsf.unica.it

sshpass -p $PASSWD ssh -o StrictHostKeyChecking=no $USERNAME@$REMOTE
