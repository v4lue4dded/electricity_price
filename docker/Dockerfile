FROM ubuntu:focal as base

# ------------------------------------------------------------------------------------------
# change working directory -----------------------------------------------------------------
# ------------------------------------------------------------------------------------------
WORKDIR /home

# ------------------------------------------------------------------------------------------
# Setup environment ------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
SHELL ["/bin/bash", "-c"]

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ------------------------------------------------------------------------------------------
# install basic libraries ------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y apt-utils
RUN apt-get update && apt-get install -y sudo
RUN apt-get update && apt-get install -y build-essential
RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nano
RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y cron
RUN apt-get update && apt-get install -y moreutils
RUN apt-get update && apt-get install -y tmux
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get update && apt-get install -y alsa-utils


# ------------------------------------------------------------------------------------------
# install miniconda ------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN  wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh && \
  mkdir /root/.conda && \
  bash Miniconda3-py38_4.12.0-Linux-x86_64.sh -b
RUN  rm -f Miniconda3-py38_4.12.0-Linux-x86_64.sh
RUN conda --version

# ------------------------------------------------------------------------------------------
# setup conda environment ------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# create conda environment 
ADD electricity_price_env.yml .
RUN conda env create -f electricity_price_env.yml
RUN rm electricity_price_env.yml

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# ------------------------------------------------------------------------------------------
# install vscode ---------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# install extra packages needed 
RUN apt-get update && apt-get install -y libxshmfence-dev 
# needed for vscode
RUN apt-get update && apt-get install -y libasound2 
# install vscode
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
  sudo install -o root -g root -m 644 microsoft.gpg /usr/share/keyrings/microsoft-archive-keyring.gpg && \
  sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' && \
  sudo apt-get update && \
  sudo apt-get install -y apt-transport-https  && \
  sudo apt-get install -y code
ADD install_vscode_extensions.sh .
RUN source install_vscode_extensions.sh
RUN rm install_vscode_extensions.sh

# install vscode-server
ADD download_and_install_vs_code_server.sh .
RUN . download_and_install_vs_code_server.sh
RUN rm download_and_install_vs_code_server.sh


# ------------------------------------------------------------------------------------------
# make shell work nicely -------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
ADD .inputrc /root/
ADD enter_conda_env.sh /root/
RUN echo 'source /root/enter_conda_env.sh' >> /root/.bashrc

RUN mkdir -p /home/log

RUN touch test.txt

####################### 
FROM base as electricity_price
# CMD ["ls"]
# RUN ls
# CMD ["/root/miniconda3/envs/electricity_price_env/bin/python", "/home/electricity_price_docker/src/test.py"]
# CMD ["conda", "run", "--no-capture-output", "--live-stream", "-n", "electricity_price_env", "python", "/home/electricity_price_docker/src/test.py"]
# CMD ["conda", "run", "--no-capture-output", "-n", "electricity_price_env", "python", "/home/electricity_price_docker/src/test.py"]
