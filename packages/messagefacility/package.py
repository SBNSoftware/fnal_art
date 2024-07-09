# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Messagefacility(CMakePackage, FnalGithubPackage):
    """A configurable message logging facility for the art suite."""

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/messagefacility"

    version_patterns = ["v2_08_00"]

    version("2.11.00", sha256="6b3f7a8ef870bbea7e1127f4f841d1ecac4fca57509b4108cd284d6b7813d360")
    version("2.10.05", sha256="cd99c85b81f7d4d23195fb6f84d8815c73d6eedbb4c543dc10c9616a5c31368d")
    version("2.10.04", sha256="5c63a26c974c69677eeb8c927a581aa40bd7ff8f6abf6ebcdd20cc423e145df9")
    version("2.10.03", sha256="94700d414a59111200dff1d77839d2edcb72f05530c039f6bdddb470be6e2252")
    version("2.10.02", sha256="1dfed808595316ce1d619e48a20b3f0cfd18afa32d807d6c3e822fd41b042fa2")
    version("2.10.01", sha256="b9572b4ccf0e61edcaf4fc4548d616be00754c9ae04aa594640d992c1047c315")
    version("2.09.00", sha256="0d596b10691d92b73a396c974846211ea7d65e819685a39b3fa1d9d4126746f0")
    version("2.08.04", sha256="dcf71449b0f73b01e2d32d1dc5b8eefa09a4462d1c766902d916ed6869b6c682")
    version("2.08.03", sha256="bf10264d94e77e14c488e02107e36e676615fa12c9e2795c4caccf0c913ba7b9")
    version("2.08.00", sha256="a2c833071dfe7538c40a0024d15f19ba062fd5f56b26f83f5cb739c12ff860ec")
    version("develop", branch="develop")

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@2.11.00:")

    depends_on("boost+filesystem+program_options+system")
    depends_on("catch2@3.3.0:", when="@2.10.00:")
    depends_on("catch2@2.3.0:2", when="@:2.09", type=("build", "test"))
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules", type="build")
    conflicts("cetmodules@:3.21.00", when="catch2@3:")
    depends_on("fhicl-cpp@4.16.00:", when="@2.08.05:")
    depends_on("fhicl-cpp@4.15", when="@2.08.01:2.08.04")
    depends_on("fhicl-cpp@:4.14", when="@:2.08.00")
    depends_on("hep-concurrency@1.07.05:", when="@2.08.00:2.10.03")
    depends_on("hep-concurrency@:1.07.04", when="@:2.07")
    depends_on("perl", type=("build", "run"))
    depends_on("py-pybind11", type="build")

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
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Perl modules.
        env.prepend_path("PERL5LIB", prefix.perllib)

    @sanitize_paths
    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Perl modules.
        env.prepend_path("PERL5LIB", prefix.perllib)

    @sanitize_paths
    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Perl modules.
        env.prepend_path("PERL5LIB", prefix.perllib)
