#!/bin/bash
# rename eigen directories in tensorflow
# to avoid conflicts with our distribution of eigen


echo
echo "working in ${PWD}"
echo

# rename Eigen namespace
echo "rename Eigen namespace"
for pfile in `grep -l -r "Eigen::" *`
do
  sed -i -e s%Eigen::%Eigen_tf::%g $pfile
done
for pfile in `grep -l -r "namespace Eigen" *`
do
  sed -i -e s%namespace\ Eigen%namespace\ Eigen_tf%g $pfile
done

echo "rename third_party eigen3 directories"
mv third_party/eigen3/Eigen third_party/eigen3/Eigen_tf || exit 1
mv third_party/eigen3/unsupported/Eigen third_party/eigen3/unsupported/Eigen_tf || exit 1

echo "rename downloaded eigen directories"
mv tensorflow/contrib/makefile/downloads/eigen/Eigen tensorflow/contrib/makefile/downloads/eigen/Eigen_tf || exit 1
mv tensorflow/contrib/makefile/downloads/eigen/unsupported/Eigen tensorflow/contrib/makefile/downloads/eigen/unsupported/Eigen_tf || exit 1
echo "directories successfully renamed"
echo
echo "rename include directives"
for pfile in `grep -l -r \<Eigen\/ *`
do
  sed -i -e s%\<Eigen\/%\<Eigen_tf\/%g $pfile
done
for pfile in `grep -l -r \#include\ \"Eigen\/ *`
do
  sed -i -e s%include\ \"Eigen\/%include\ \"Eigen_tf\/%g $pfile
done
for pfile in `grep -l -r \/Eigen\/ *`
do
  sed -i -e s%\/Eigen\/%\/Eigen_tf\/%g $pfile
done
echo "rename_eigen.sh completed successfully"
echo
exit 0


