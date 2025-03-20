FROM ubuntu:latest
LABEL authors="KOVALEV"

ENTRYPOINT ["top", "-b"]