ifdef MSVC     # Avoid the MingW/Cygwin sections
    uname_S := Windows
else                          # If uname not available => 'not'
    uname_S := $(shell sh -c 'uname -s 2>/dev/null || echo not')
endif

# Avoid nesting "if .. else if .. else .. endif endif"
# because maintenance of matching if/else/endif is a pain
ifneq (,$(findstring CYGWIN,$(uname_S)))
  
    SSHPATH := /c/Users/$$(echo $$USER)/.ssh
endif
ifeq ($(uname_S),Linux)
    SSHPATH := $$(echo $$HOME)/.ssh
endif

all:
	echo $(uname_S)
	echo $(SSHPATH)
	#docker build -t appflow-dev-environment .
	#nohup docker run --privileged -dt -v $(SSHPATH):/root/.ssh appflow-dev-environment
	# docker
	#nohup
	#docker run -dt -v /c/Users/$$(echo $$USER)/.ssh:/root/.ssh appflow-dev-environment
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
