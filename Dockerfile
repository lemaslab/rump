# Dockerfile for UMPIRE

FROM rocker/r-ver:3.5.2

MAINTAINER xinsongdu@ufl.edu

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    vim \
    libfreetype6 \
    libcairo2-dev \
    libexpat1-dev \
    libgmp3-dev \
    liblapack-dev \
    libnetcdf-dev \
    libopenbabel-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libgsl0-dev \
    libmpfr-dev \
    pkg-config \
    fftw3-dev \
    libgtk2.0-dev \
    libtiff5-dev \
    libnetcdf-dev \
    libmpfr-dev \
    libnetcdf-dev \
    liblapack-dev \
    cmake \
    default-jdk \
    python\
    python-dev\
    software-properties-common\
    python-pip\
    python3-pip\
    python-tk\
    python3-tk\

    libnetcdf-dev libpng-dev libbz2-dev liblzma-dev libpcre3-dev libicu-dev

# Install python3-based necessary dependencies for UMPIRE
RUN pip3 install --upgrade setuptools
RUN pip3 install 'numpy==1.18.1' 'scipy==1.4.1' 'pandas==0.25.3' 'matplotlib<3.0.0,>=2.1.1' 'plotly==4.5.0' 'seaborn==0.9.1' 'scikit-learn==0.22.1' matplotlib_venn 'multiqc==1.8' 'statsmodels==0.11.0' 'fastcluster==1.1.26'
RUN echo "alias python=python3" >> ~/.bash_profile

ENV NETCDF_INCLUDE=/usr/include

# invalidates cache every 24 hours
ADD http://master.bioconductor.org/todays-date /tmp/

# build dirs for UFRC
RUN mkdir /ufrc /orange /bio /rlts 
RUN mkdir -p /scratch/local
RUN mkdir app

# define work dir
WORKDIR /app
COPY accessibility.properties /app

# Fix a bug for java
RUN mv accessibility.properties /etc/java-8-openjdk/

# Install mummichog
RUN pip install --upgrade setuptools
RUN pip install mummichog

RUN echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc