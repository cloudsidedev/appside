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

all:
	docker build -t appflow-dev-environment .
	nohup docker run --name appflow-dev-environment -dt -v $(SSHPATH):/root/.ssh appflow-dev-environment

clean:
	../bin/docker-cleanup.sh

cleanup_all:
	../bin/docker-cleanup.sh all

shell:
	$(DOCKER_COMMAND) exec -ti appflow-dev-environment sh -c "exec >/dev/tty 2>/dev/tty </dev/tty && tmate -S /tmp/tmate.sock new-session -d && tmate -S /tmp/tmate.sock wait tmate-ready && tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'"

stop:
	docker ps -a -f ancestor=appflow-dev-environment -q | xargs docker stop

ip:
	docker ps -a -f ancestor=appflow-dev-environment -q | xargs docker inspect
