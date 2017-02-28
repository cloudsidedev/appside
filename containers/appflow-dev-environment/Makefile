all:
	docker build -t appflow-dev-environment .
	nohup docker run -dt appflow-dev-environment 
	docker
clean:
	../bin/docker-cleanup.sh

cleanup_all:
	../bin/docker-cleanup.sh all

shell:
	docker exec -ti appflow-dev-environment	 sh

stop:
	docker ps -a -f ancestor=appflow-dev-environment -q | xargs docker stop
	
ip:
	docker ps -a -f ancestor=appflow-dev-environment -q | xargs docker inspect
