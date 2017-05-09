ifdef MSVC     # Avoid the MingW/Cygwin sections
    uname_S := Windows
else                          # If uname not available => 'not'
    uname_S := $(shell sh -c 'uname -s 2>/dev/null || echo not')
endif

# Avoid nesting "if .. else if .. else .. endif endif"
# because maintenance of matching if/else/endif is a pain

ifeq ($(uname_S),CYGWIN*)
    CC := cl
		echo foo
endif
ifeq ($(uname_S),OSF1)
    CFLAGS += -D_OSF_SOURCE
endif
ifeq ($(uname_S),Linux)
    CFLAGS += -DNDEBUG
endif
ifeq ($(uname_S),GNU/kFreeBSD)
    CFLAGS += -D_BSD_ALLOC
endif
ifeq ($(uname_S),UnixWare)
    CFLAGS += -Wextra
endif


all:
	echo $(uname_S)
	docker build -t appflow-dev-environment .
	nohup docker run --name appflow-dev-environment -dt -v $$(echo $$HOME)/.ssh:/root/.ssh appflow-dev-environment

	#exec >/dev/tty 2>/dev/tty </dev/tty && \
	#tmate -S /tmp/tmate.sock new-session -d && \
	#tmate -S /tmp/tmate.sock wait tmate-ready && \
	#tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'

	# docker
	#nohup
	#docker run -dt -v /c/Users/$$(echo $$USER)/.ssh:/root/.ssh appflow-dev-environment
clean:
	../bin/docker-cleanup.sh

cleanup_all:
	../bin/docker-cleanup.sh all

shell:
	docker exec -ti appflow-dev-environment	sh

stop:
	docker ps -a -f ancestor=appflow-dev-environment -q | xargs docker stop

ip:
	docker ps -a -f ancestor=appflow-dev-environment -q | xargs docker inspect
