# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class HepHpc(CMakePackage):
    """Utilities for storing ntuples in HDF5 files"""

    homepage = "https://github.com/art-framework-suite/hep-hpc"
    url = "https://github.com/art-framework-suite/hep-hpc/archive/refs/tags/v0_14_02.tar.gz"
    git = "https://github.com/art-framework-suite/hep-hpc.git"

    maintainers = ["marcmengel"]

    version("0_14_02", sha256="2d89f7c4d40ad1c585b0bf2d1412124ffa6a0cc6d483ced30c3110ca89cee26f")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    variant("mpi", default=False, description="build with MPI support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("googletest", type="build")
    depends_on("hdf5")
    depends_on("mpi", when="+mpi")

    def patch(self):
        # use external for googletest...
        filter_file(
           r'add_subdirectory\(gtest.*',
           'find_package(GTest)',
           'CMakeLists.txt'
        )
        filter_file(
            r'include_directories\(gtest/googletest/include\)',
            'include_directories(get_target_property(GTest::gtest INTERFACE_INCLUDE_DIRECTORIES))',
            'test/CMakeLists.txt'
        )
        tcml = [
             'test/hdf5/CMakeLists.txt', 
             'test/MPI/CMakeLists.txt', 
             'test/Utilities/CMakeLists.txt'
        ]
        for f in tcml:
            filter_file(
                r'target_link_libraries\((.*) gtest\)',
                r'target_link_libraries(\1 GTest::gtest)',
                f
            )


    def cmake_args(self):
        args = [
           self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        if self.spec.satisfies("+mpi"):
             args.append("-DWANT_MPI")
        return args
