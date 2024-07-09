# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelTbbOneapi(CMakePackage):
    """Widely used C++ template library for task parallelism.
    Intel Threading Building Blocks (Intel TBB) lets you easily write parallel
    C++ programs that take full advantage of multicore performance, that are
    portable and composable, and that have future-proof scalability.
    """

    homepage = "http://www.threadingbuildingblocks.org/"
    url = "https://github.com/oneapi-src/oneTBB/archive/v2021.3.0.tar.gz"

    # Note: when adding new versions, please check and update the
    # patches, filters and url_for_version() below as needed.
    version("2021.9.0", sha256="1ce48f34dada7837f510735ff1172f6e2c261b09460e3bf773b49791d247d24e")
    version(
        "2021.7.0-rc1", sha256="20449198579f2f5321c46a0b07b4d100af771018451629a8db38cc331178b17d"
    )
    version("2021.6.0", sha256="4897dd106d573e9dacda8509ca5af1a0e008755bf9c383ef6777ac490223031f")
    version("2021.5.0", sha256="e5b57537c741400cf6134b428fc1689a649d7d38d9bb9c1b6d64f092ea28178a")
    version("2021.4.0", sha256="021796c7845e155e616f5ecda16daa606ebb4c6f90b996e5c08aebab7a8d3de3")
    version("2021.3.0", sha256="8f616561603695bbb83871875d2c6051ea28f8187dbe59299961369904d1d49e")
    version("2021.2.0", sha256="cee20b0a71d977416f3e3b4ec643ee4f38cedeb2a9ff015303431dd9d8d79854")
    version("2021.1.1", sha256="b182c73caaaabc44ddc5ad13113aca7e453af73c1690e4061f71dfe4935d74e8")

    provides("tbb")

    variant(
        "cxxstd",
        default="default",
        values=("default", "98", "11", "14", "17", "20", "23"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("examples", default=False, description="Build examples")

    # Build and install CMake config files if we're new enough.
    depends_on("cmake@3.0.0:", type="build")
    depends_on("hwloc")
    depends_on("binutils+gas@2.31:", when="os=scientific7", type="build")
    depends_on("binutils+gas@2.31:", when="os=centos7", type="build")
    depends_on("binutils+gas@2.31:", when="os=rhel7", type="build")

    def cmake_args(self):
        spec = self.spec
        options = [
            self.define("CMAKE_HWLOC_2_INCLUDE_PATH", spec["hwloc"].prefix.include),
            self.define("CMAKE_HWLOC_2_LIBRARY_PATH", spec["hwloc"].libs),
            self.define("TBB_CPF", False),
            self.define("TBB_DISABLE_HWLOC_AUTOMATIC_SEARCH", True),
            self.define("TBB_FIND_PACKAGE", False),
            self.define("TBB_INSTALL_VARS", True),
            self.define("TBB_STRICT", True),
            self.define("TBB_TEST", self.run_tests),
            self.define("TBB_VALGRIND_MEMCHECK", False),
            self.define_from_variant("TBB_EXAMPLES", "examples"),
        ]
        if spec.variants["cxxstd"].value != "default":
            options.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        return options

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        env.set("TBB_INC", prefix.include)
