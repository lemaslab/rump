# DO NOT EDIT FILES CALLED 'Dockerfile'; they are automatically
# generated. Edit 'Dockerfile.in' and generate the 'Dockerfile'
# with the 'rake' command.

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

    libnetcdf-dev libpng-dev libbz2-dev liblzma-dev libpcre3-dev libicu-dev

RUN pip3 install --upgrade setuptools
RUN pip3 install numpy scipy pandas 'matplotlib<3.0.0,>=2.1.1' plotly seaborn sklearn matplotlib_venn multiqc
RUN echo "alias python=python3" >> ~/.bash_profile

# RUN bash -i -c 'wget -O libSBML-5.10.2-core-src.tar.gz http://downloads.sourceforge.net/project/sbml/libsbml/5.10.2/stable/libSBML-5.10.2-core-src.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fsbml%2Ffiles%2Flibsbml%2F5.10.2%2Fstable%2F && tar xzvf libSBML-5.10.2-core-src.tar.gz ; cd libsbml-5.10.2 && CXXFLAGS=-fPIC CFLAGS=-fPIC ./configure --prefix=/usr && make && make install && ldconfig'

# RUN R CMD javareconf

ENV NETCDF_INCLUDE=/usr/include

# invalidates cache every 24 hours
ADD http://master.bioconductor.org/todays-date /tmp/

# build dirs for UFRC
RUN mkdir /ufrc /orange /bio /rlts 
RUN mkdir -p /scratch/local
RUN mkdir app

# define work dir
WORKDIR /app
# COPY MZmine-2.28 /app
# COPY xcms-docker.tar.gz /app
# COPY libs.R /app
COPY accessibility.properties /app

# RUN R -f /tmp/install.R # comment out this line
# use the following line to install required R libraries for xcms
# RUN Rscript libs.R
RUN mv accessibility.properties /etc/java-8-openjdk/
RUN pip install --upgrade setuptools
RUN pip install mummichog
RUN pip3 install fastcluster

RUN echo "alias python=python3" >> ~/.bashrc