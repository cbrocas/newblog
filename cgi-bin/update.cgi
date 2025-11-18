#!/bin/bash

# From https://theowinter.ch/articles/Use-cgi-bin-to-automate-Jekyll/

#Script is executed by www-data user. It needs to have write-access to
#/var/www/newblog & /var/www/blog.brocas.org/
echo "Content-type: text/plain"
echo
echo "Checking for updates to blog..."
exec 2>&1
cd /var/www/newblog

#Check if there are changes
if git checkout main &&
    git fetch origin main &&
    [ `git rev-list HEAD...origin/main --count` != 0 ] &&
    git merge origin/main
then
    echo 'Changes found, syncing.'
    #jekyll build
    rsync -av --delete /var/www/newblog/public/ /var/www/blog.brocas.org/
else
    echo 'Not updated.'
fi
echo "Have a nice day!"
