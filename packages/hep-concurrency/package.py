# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class HepConcurrency(CMakePackage, FnalGithubPackage):
    """A concurrency library for the art suite."""

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/hep-concurrency"

    version_patterns = ["v1_07_04"]

    version("1.10.00", sha256="04b050c89257ac07beef24d8dc4b8eb0184bf7e8390083da62293c02001a28bc")
    version("1.09.02", sha256="86666c0c8c8dc87358a0158d7d01df1d6cc65932f6064782b36b842ae8e5d8a2")
    version("1.09.01", sha256="1fb91a35c244013f48cb1dd34c39ece87431ce23ee383f9be23773e0a585ae43")
    version("1.09.00", sha256="075d24af843f76a8559dc1fdc91b076b91ab3152c618aed9ba6bdad61d745846")
    version("1.08.00", sha256="24e893550e6897a4f7959869f751ec6611814b696c9eebd8597b7a59ae4e7758")
    version("1.07.04", sha256="442db7ea3c0057e86165a001ef77c1fc0e5ed65c62fd1dd53e68fb8fe9a5fef3")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@1.10.00:")

    depends_on("catch2@2.3.0:2", when="@:1.08", type=("build", "test"))
    depends_on("catch2@3.3.0:", when="@1.09:", type=("build", "test"))
    depends_on("cetlib-except")
    depends_on("cetmodules@3.19.02:", type="build")
    conflicts("cetmodules@:3.21.00", when="catch2@3:")
    depends_on("tbb")

    patch("test_build.patch", when="@:1.08.00")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        # PATH for tests.
        env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
