#!/usr/bin/env bash
# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# Downloads and builds all of TensorFlow's dependencies for Linux, and compiles
# the TensorFlow library itself. Supported on Ubuntu 14.04 and 16.04.

# consider and compare various march options with gcc -c -Q -march=XXX --help=target | grep enabled
# using lowest common denominator -march=core2

set -e

# Make sure we're in the correct directory, at the root of the source tree.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${SCRIPT_DIR}/../../../

source "${SCRIPT_DIR}/build_helper.subr"
##JOB_COUNT="${JOB_COUNT:-$(get_job_count)}"
JOB_COUNT=${ncore}

makedir=tensorflow/contrib/makefile
echo                               
echo "This script is in ${SCRIPT_DIR}"
echo "now in $PWD"                    
echo "install directory is ${TENSORFLOW_FQ_DIR}"
echo "build uses ${JOB_COUNT} cores"
echo                                            

if [ -z ${TENSORFLOW_FQ_DIR} ]; then
  echo "ERROR: TENSORFLOW_FQ_DIR is not defined"
  exit 1                                        
fi                                              

# Remove any old files first.
make -f ${makedir}/Makefile clean
rm -rf ${makedir}/downloads
rm -rf ${makedir}/gen

# Pull down the required versions of the frameworks we need.
tensorflow/contrib/makefile/download_dependencies.sh

# use our build of protobuf
mkdir -p ${makedir}/gen
mv ${makedir}/downloads/protobuf ${makedir}/downloads/protobuf.do.not.use
ln -s ${PROTOBUF_FQ_DIR} ${makedir}/gen/protobuf-host
ln -s ${PROTOBUF_FQ_DIR} ${makedir}/gen/protobuf
# debugging 
echo "before build"
ls -l ${makedir}/gen
echo

# rename Eigen namespace and directories
${makedir}/rename_eigen.sh

# compile google's nsync
HOST_NSYNC_LIB=`${makedir}/compile_nsync.sh`
TARGET_NSYNC_LIB="$HOST_NSYNC_LIB"
export HOST_NSYNC_LIB TARGET_NSYNC_LIB

# Build TensorFlow.
env CC=gcc CXX=g++ FC=gfortran make -j"${JOB_COUNT}" -f tensorflow/contrib/makefile/Makefile \
  OPTFLAGS="-O3 -march=core2" \
  HOST_CXXFLAGS="--std=c++17 -march=core2" \
  SUB_MAKEFILES=./tensorflow/contrib/makefile/sub_makefiles/so/Makefile.in \
  libtensorflow-core.so

# debugging 
echo "after build"
ls -l ${makedir}/gen
echo
# remove the links now to avoid confusion
rm -f ${makedir}/gen/protobuf-host
rm -f ${makedir}/gen/protobuf

# installation step
${makedir}/install_all.sh || ssi_die "install failed"

# make clean
cd ${SCRIPT_DIR}/../../../
make -f tensorflow/contrib/makefile/Makefile \
  SUB_MAKEFILES=./tensorflow/contrib/makefile/sub_makefiles/so/Makefile.in \
  clean

exit 0


