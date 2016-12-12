FROM ubuntu:latest

RUN apt-get update

# Create a user
RUN adduser --disabled-login --gecos 'shkh' shkh \
	&& passwd -d shkh \
	&& gpasswd -a shkh sudo 
USER shkh 
WORKDIR /home/shkh
CMD "/bin/bash"

#Install dependencies before OpenCV

RUN apt-get install -y wget curl build-essential cmake python2.7 python2.7-dev
RUN wget 'https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg' && \
	/bin/sh setuptools-0.6c11-py2.7.egg && rm -f setuptools-0.6c11-py2.7.egg
RUN curl 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py' | python2.7

RUN apt-get install -y -q libavformat-dev libavcodec-dev libavfilter-dev libswscale-dev \
	libjpeg-dev libpng-dev libtiff-dev libjasper-dev zlib1g-dev libopenexr-dev \
	libxine-dev libeigen3-dev libtbb-dev

#Install OpenCV stuff

RUN curl -L 'http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.7/opencv-2.4.7.tar.gz/' | \
	tar xvzf - mkdir -p opencv-2.4.7/release
WORKDIR /home/shkh/opencv-2.4.7/release
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D WITH_XINE=ON -D WITH_TBB=ON ..
RUN make && make install

WORKDIR /home/shkh
