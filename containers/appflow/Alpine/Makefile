#
# https://github.com/whilp/ssh-agent
#
#
#
#



ifdef MSVC     # Avoid the MingW/Cygwin sections
    uname_S := Windows
else                          # If uname not available => 'not'
    uname_S := $(shell sh -c 'uname -s 2>/dev/null || echo not')
endif

# Avoid nesting "if .. else if .. else .. endif endif"
# because maintenance of matching if/else/endif is a pain

SSHPATH := $$(echo $$HOME)/.ssh
DOCKER_COMMAND := docker

ifneq (,$(findstring CYGWIN,$(uname_S)))
    SSHPATH := /c/Users/$$(echo $$USER)/.ssh
    DOCKER_COMMAND := winpty docker
endif
ifeq ($(uname_S),Linux)
    SSHPATH := $$(echo $$HOME)/.ssh
    DOCKER_COMMAND := docker
endif

build:
	docker build -t appflow .

all:
	docker build -t appflow .
	nohup docker run --name appflow -dt -v $(SSHPATH):/root/.ssh appflow

run:
	-docker stop appflow
	-docker rm appflow
	# nohup docker run --name appflow -dt -v $(SSHPATH):/root/.ssh appflow
	# nohup docker run --name appflow -dt -v $(SSHPATH):/root/.ssh --entrypoint=bash appflow
	# nohup docker run --name appflow -dt -v $(SSHPATH):/root/.ssh --entrypoint=run.sh appflow
	# nohup docker run --name appflow -i -t -v $$(readlink $$SSH_AUTH_SOCK):/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent appflow
	# nohup docker run --name appflow -i -t -v $SSH_AUTH_SOCK:/ssh-agent --env SSH_AUTH_SOCK=/ssh-agent appflow
	# nohup docker run --name appflow -i -t --volumes-from=ssh-agent --env SSH_AUTH_SOCK=/.ssh-agent/socket appflow
	# docker run --name appflow -i -t --volumes-from=ssh-agent --env SSH_AUTH_SOCK=/ssh/auth/sock appflow
	# THIS WORKS (get's key from ssh-agent container):
	# docker run --name appflow --rm -it --volumes-from=ssh-agent --env SSH_AUTH_SOCK=/ssh/auth/sock --entrypoint=bash appflow
	docker run --name appflow --rm -it --volumes-from=ssh-agent -v $$HOME/.appflow:/home/appflow/.appflow -v $$HOME/dotfiles:/home/appflow/dotfiles --env SSH_AUTH_SOCK=/ssh/auth/sock appflow

exec:
	docker exec -ti appflow ssh-add -L
	# docker exec -ti appflow ls

clean:
	../bin/docker-cleanup.sh

cleanup_all:
	../bin/docker-cleanup.sh all

shell:
	$(DOCKER_COMMAND) exec -ti appflow sh -c "exec >/dev/tty 2>/dev/tty </dev/tty && tmate -S /tmp/tmate.sock new-session -d && tmate -S /tmp/tmate.sock wait tmate-ready && tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'"

stop:
	docker ps -a -f ancestor=appflow -q | xargs docker stop

ip:
	docker ps -a -f ancestor=appflow -q | xargs docker inspect
