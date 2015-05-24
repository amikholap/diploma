FROM ubuntu:latest

RUN apt-get update -qq
RUN apt-get install --no-install-recommends -y -qq \
    git \
    build-essential \
    cmake \
    pkg-config \
    # rtl_sdr
    libusb-1.0-0-dev \
    # DSD
    wget \
    libsndfile1-dev \
    fftw3-dev \
    liblapack-dev \
    portaudio19-dev \
    # utils
    socat

# rtl-sdr
WORKDIR /tmp
RUN git clone git://git.osmocom.org/rtl-sdr.git
WORKDIR rtl-sdr
RUN mkdir build
WORKDIR build
RUN cmake ..
RUN make
RUN make install

# IT++
WORKDIR /tmp
RUN wget --no-verbose -O itpp-latest.tar.bz2 http://sourceforge.net/projects/itpp/files/latest/download?source=files
RUN tar xjf itpp-latest.tar.bz2
RUN cd itpp-* && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make .. && \
    make install

# mbelib
WORKDIR /tmp
RUN git clone git://github.com/szechyjs/mbelib
WORKDIR mbelib
RUN mkdir mbelib
WORKDIR build
RUN cmake ..
RUN make
RUN make install

# DSD
WORKDIR /tmp
RUN git clone git://github.com/szechyjs/dsd
WORKDIR dsd
RUN mkdir dsd
WORKDIR build
RUN cmake ..
RUN make
RUN make install

RUN ldconfig

WORKDIR /

CMD socat UDP-RECV:7355 - | dsd -q -i /dev/stdin -o /dev/stdout | socat - UDP-SENDTO:127.0.0.1:7356
