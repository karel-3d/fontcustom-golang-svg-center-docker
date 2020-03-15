FROM golang:1.13.8
LABEL maintainer="kb@karelbilek.com"

RUN apt-get update \
    && apt-get install -y \
      zlib1g-dev \
      fontforge \
      git \
      build-essential \
      rubygems \
      ruby-dev \
       inkscape \
      gir1.2-rsvg-2.0 \
      python3-cairo \
      python3-gi \
      python3-gi-cairo \
    && git clone https://github.com/bramstein/sfnt2woff-zopfli.git \
    && cd sfnt2woff-zopfli \
    && make \
    && mv sfnt2woff-zopfli /usr/local/bin/sfnt2woff \
    && cd .. \
    && rm -rf sfnt2woff-zopfli \
    && git clone --recursive https://github.com/google/woff2.git \
    && cd woff2 \
    && make clean all \
    && mv woff2_compress /usr/local/bin/ \
    && mv woff2_decompress /usr/local/bin/ \
    && cd .. \
    && rm -rf woff2 \
    && gem install fontcustom \
    && apt-get remove -y zlib1g-dev git build-essential ruby-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && apt-get -y autoclean

COPY svgcenter.py /svgcenter.py

VOLUME ["/project"]
WORKDIR /project

