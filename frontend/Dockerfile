# syntax=docker/dockerfile:1
FROM node:16.16.0

WORKDIR /ember-app

RUN \
    apt-get update -y &&\
    apt-get install -y python-dev

# install chrome for default testem config (as of ember-cli 2.15.0)
RUN \
    apt-get update &&\
    apt-get install -y \
    apt-transport-https \
    gnupg \
    --no-install-recommends &&\
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list &&\
    apt-get update &&\
    apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# tweak chrome to run with --no-sandbox option
RUN \
    sed -i 's/"$@"/--no-sandbox "$@"/g' /opt/google/chrome/google-chrome

# set container bash prompt color to blue in order to
# differentiate container terminal sessions from host
# terminal sessions
RUN \
    echo 'PS1="\[\\e[0;94m\]${debian_chroot:+($debian_chroot)}\\u@\\h:\\w\\\\$\[\\e[m\] "' >> ~/.bashrc

# install ember-cli
RUN npm install -g npm && \
    npm install -g ember-cli@4.5.0

COPY package.json ./package.json

RUN npm install && npm cache clean --force

COPY . .

# run ember server on container start
ENTRYPOINT ["ember", "serve"]

# ember server on port 4200
# livereload server on port 7020 (changed in v2.17.0 from 49153)
# test server on port 7357
EXPOSE 4200 7020 7357
