#!/bin/bash

if [ "$1" == "all" ]
then

    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
    docker rmi $(docker images -q)
    docker volume rm $(docker volume ls -qf dangling=true)

else

    # stop and rm all containers
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)

    # stop and rm exited containers
    # docker stop $(docker ps -q -f status=exited)
    # docker rm $(docker ps -q -f status=exited)

fi
