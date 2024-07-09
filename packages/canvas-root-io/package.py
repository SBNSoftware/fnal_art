# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class CanvasRootIo(CMakePackage, FnalGithubPackage):
    """A Root I/O library for the art suite."""

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/canvas-root-io"

    version_patterns = ["v1_09_04"]

    version("develop", branch="develop", get_full_repo=True)

    version("1.14.00", sha256="77ce8277704451aaa0eb003298b47accbf302a55f044fc330bf43040495684bd")
    version("1.13.06", sha256="a0b7fdbc0f8f52b39a289f97c1354e304794beae87e8128099ffada5460ef72f")
    version("1.13.05", sha256="34c8b31cd6e769a1fc0afb3758071827202f11bcc218f37bbac6071a9a55fecf")
    version("1.13.03", sha256="4ef6333ac780591821364d51ef926b512a1e806b1b39f1ba8dacc97f9a0e20a7")
    version("1.13.01", sha256="44795decae980c7f7a90dde69c886b7f01b150caef7ec8f88622740fdcb87549")
    version("1.12.03", sha256="53919330ebc85fb19fb4ab42a4be588cf12e866118339ccd408af0722eebdb5b")
    version("1.12.02", sha256="ad0fdb8d03e2646ca1522cabd1bcf766884a2c5720a3c0d338e7d29995e10316")
    version("1.12.01", sha256="244dde7f035ef142c42f8bdb8cd80bda2e39ef4e1bd0f45d16614d495221358a")
    version("1.11.02", sha256="c647f74c39d960a56c9599470652c5dea5bcfa3a75a570a7b6ca4aa4093a05d7")
    version("1.11.00", sha256="950ccf0277f7315d396ae49f6421fd613a7bb34cf7cba68c1c2dfb062b990b6c")
    version("1.09.04", sha256="cb854b4fdc72be24856886d985f96ceb3b0049729df0b4a11fb501ff7c48847b")

    patch("test_build.patch", when="@:1.11.00")

    requires("%gcc@:12", when="@:1.09")

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@1.14.00:")

    depends_on("boost+thread")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules@3.19.02:", type="build")
    depends_on("clhep")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency")
    depends_on("catch2", type=("build", "test"))
    depends_on("messagefacility")
    depends_on("root@6.30:+python", when="@1.14:")
    depends_on("root@6.28:+python", when="@1.12:")
    depends_on("root@6.26:+python", when="@1.11:")
    depends_on("root@6.22:+python", when="@1.09:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        # Binaries.
        env.prepend_path("PATH", prefix.bin)
        # Set LD_LIBRARY_PATH so CheckClassVersion.py can find cppyy lib
        env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            env.prepend_path("ROOT_INCLUDE_PATH", self.spec[d.name].prefix.include)

    @sanitize_paths
    def setup_run_environment(self, env):
        prefix = self.prefix
        # Set LD_LIBRARY_PATH so that dictionaries are available downstream
        env.prepend_path("LD_LIBRARY_PATH", prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            env.prepend_path("ROOT_INCLUDE_PATH", self.spec[d.name].prefix.include)
        env.prepend_path("ROOT_INCLUDE_PATH", prefix.include)

    @sanitize_paths
    def setup_dependent_build_environment(self, env, dependent_spec):
        # Set LD_LIBRARY_PATH so CheckClassVersion.py can find cppyy lib
        env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in dependent_spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            env.prepend_path("ROOT_INCLUDE_PATH", dependent_spec[d.name].prefix.include)
