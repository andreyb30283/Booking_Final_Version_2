FROM ubuntu:latest
LABEL authors="ICH"

ENTRYPOINT ["top", "-b"]