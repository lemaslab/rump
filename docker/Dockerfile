# DO NOT EDIT FILES CALLED 'Dockerfile'; they are automatically
# generated. Edit 'Dockerfile.in' and generate the 'Dockerfile'
# with the 'rake' command.

# The suggested name for this image is: bioconductor/release_metabolomics.

FROM bioconductor/release_protmetcore2

MAINTAINER xinsongdu@ufl.edu

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
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
    libnetcdf-dev libpng-dev libbz2-dev liblzma-dev libpcre3-dev libicu-dev

RUN bash -i -c 'wget -O libSBML-5.10.2-core-src.tar.gz http://downloads.sourceforge.net/project/sbml/libsbml/5.10.2/stable/libSBML-5.10.2-core-src.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fsbml%2Ffiles%2Flibsbml%2F5.10.2%2Fstable%2F && tar xzvf libSBML-5.10.2-core-src.tar.gz ; cd libsbml-5.10.2 && CXXFLAGS=-fPIC CFLAGS=-fPIC ./configure --prefix=/usr && make && make install && ldconfig'

RUN R CMD javareconf

ENV NETCDF_INCLUDE=/usr/include

#ADD install.R /tmp/ # comment out this line
ADD libs.R /tmp/

# invalidates cache every 24 hours
ADD http://master.bioconductor.org/todays-date /tmp/

# RUN R -f /tmp/install.R # comment out this line
# use the following line to install required R libraries for xcms
RUN R -f /tmp/libs.R

# build dirs for UFRC
RUN mkdir /ufrc /orange /bio /rlts 
RUN mkdir -p /scratch/local
RUN mkdir app

# define work dir
WORKDIR /app
COPY . /app

# Docker for MZmine 2, reference: https://github.com/biorack/metatlas/blob/master/docker/mzmine/Dockerfile
RUN echo "===> add webupd8 repository..."  && \
    echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee /etc/apt/sources.list.d/webupd8team-java.list  && \
    echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list  && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886  && \
    apt-get update


RUN echo "===> install Java"  && \
    echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections  && \
    echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections  && \
    DEBIAN_FRONTEND=noninteractive  apt-get install -y --force-yes oracle-java8-installer oracle-java8-set-default


RUN echo "===> clean up..."  && \
    rm -rf /var/cache/oracle-jdk8-installer  && \
    apt-get clean  && \
    rm -rf /var/lib/apt/lists/*


# define default command
#CMD ["java"]

ENV MZMINE_VERSIONS /home/$NB_USER/work/mzmine_components/versions
RUN mkdir -p $MZMINE_VERSIONS && \
    cd $MZMINE_VERSIONS && \
    wget $(curl -s https://api.github.com/repos/mzmine/mzmine2/releases/latest | grep 'browser_' | cut -d\" -f4) -O mzmine_latest.zip && \
    unzip mzmine_latest.zip
#cp ../MZmine-2.23/startMZmine_NERSC_* .
# run app
# CMD ["Rscript", "xcms-direct-injection.R"]