.PHONY: clean test
export PYTHONPATH := $(shell pwd)/test:$(shell pwd):$(PYTHONPATH)

test:
		python -m pytest test/test_1.py
clean:
		@if docker image inspect redhat/ubi8 > /dev/null 2>&1; then docker rmi redhat/ubi8; fi
		@if docker image inspect redhat/ubi9 > /dev/null 2>&1; then docker rmi redhat/ubi9; fi
		@if docker image inspect rockylinux:8 > /dev/null 2>&1; then docker rmi rockylinux:8; fi
		@if docker image inspect rockylinux:9 > /dev/null 2>&1; then docker rmi rockylinux:9; fi
		@if docker image inspect oraclelinux:8 > /dev/null 2>&1; then docker rmi oraclelinux:8; fi
		@if docker image inspect oraclelinux:9 > /dev/null 2>&1; then docker rmi oraclelinux:9; fi
		@if docker image inspect fedora:latest > /dev/null 2>&1; then docker rmi fedora:latest; fi
		@if docker image inspect ubuntu:focal > /dev/null 2>&1; then docker rmi ubuntu:focal; fi
		@if docker image inspect ubuntu:jammy > /dev/null 2>&1; then docker rmi ubuntu:jammy; fi
		@if docker image inspect debian:bullseye > /dev/null 2>&1; then docker rmi debian:bullseye; fi
		@if docker image inspect opensuse/leap:latest > /dev/null 2>&1; then docker rmi opensuse/leap:latest; fi
		@if docker image inspect registry.suse.com/suse/sle15:latest > /dev/null 2>&1; then docker rmi registry.suse.com/suse/sle15:latest; fi
		@if docker image inspect registry.suse.com/suse/sle15:15.3 > /dev/null 2>&1; then docker rmi registry.suse.com/suse/sle15:15.3; fi
		@if docker image inspect amazonlinux:2 > /dev/null 2>&1; then docker rmi amazonlinux:2; fi
		@if docker image inspect amazonlinux:2023 > /dev/null 2>&1; then docker rmi amazonlinux:2023; fi
		docker system prune -f
