#!/bin/bash
#
# TENSORFLOW_FQ_DIR is defined by the fake setup in build_tensorflow.sh

cd ${TENSORFLOW_FQ_DIR}
echo
echo "working in ${PWD}"
echo

# get the headers
cd ${TENSORFLOW_FQ_DIR}/tensorflow-*
tdir=${PWD}
echo "now working in tdir ${tdir}"
echo
makedir=${tdir}/tensorflow/contrib/makefile
gendir=${tdir}/tensorflow/contrib/makefile/gen/host_obj
dwndir=${tdir}/tensorflow/contrib/makefile/downloads
incdir=${TENSORFLOW_FQ_DIR}/include
mkdir -p ${incdir} || exit 1

# move the libraries
mkdir -p ${TENSORFLOW_FQ_DIR}/lib || exit 1
cp -p ${makedir}/gen/lib/libtensorflow-core.* ${TENSORFLOW_FQ_DIR}/lib || exit 1

# tensorflow headers
cd ${tdir}
# cannot filter out contrib subdir here, using makefile instead
header_list=`find tensorflow -type f -name "*.h" | grep -v makefile`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# generated headers
cd ${gendir}
header_list=`find tensorflow -type f -name "*.h"`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# third party headers
cd ${tdir}
header_list=`find third_party -type f -name "*.h" | grep -v contrib`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# third party eigen headers
header_list=`find third_party/eigen3 -type f | grep -v contrib`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# downloaded headers
cd ${dwndir}
header_list=`find absl  cub  double_conversion  fft2d  gemmlowp googletest re2 -type f -name "*.h"`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# downloaded eigen headers
header_list=`find eigen/Eigen_tf eigen/unsupported -type f`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# eigen signature file
cp -p eigen/signature_of_eigen3_matrix_library ${incdir}/eigen/ || exit 1

echo "install_all.sh completed successfully"
echo
exit 0
