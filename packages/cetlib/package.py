# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Cetlib(CMakePackage, FnalGithubPackage):
    """A utility library for the art suite."""

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/cetlib"

    version_patterns = ["v3_13_04"]

    version("3.19.00", sha256="696ef0e98dde96a5f34fa38db9adfdcceed325b04c64f0b70d9cc27986d8f28c")
    version("3.18.02", sha256="230c0d5d5082e878e1afa7fe9b5b54e52f9ec70373c7000a5775351817fb95d7")
    version("3.18.01", sha256="7e8b39e6ad0dce26d7fa41985d962fd2f97113403511bad0134c86ccee0e17ae")
    version("3.18.00", sha256="bf559b054af5881ef9e1b7ef91bb722fd255e178edbeca204d201584ee277fee")
    version("3.17.01", sha256="c29add5c9085e1fadc8f5fbdb1cd9b666d2290bd252022cef1feb0c30368d597")
    version("3.17.00", sha256="04160b9607948b329465b60271ca735c449f3bf7d53e31a44ec3107cc6aafe26")
    version("3.16.00", sha256="a0e670a5144b215c9a6641d0b9b35512790d9ba4b638e213651f5040417f4070")
    version("3.13.04", sha256="40ca829cfb172f6cbf516bd3427fc7b7e893f9c916d969800261194610c45edf")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@3.19.00:")

    patch("test_build.patch", when="@:3.16.00")

    depends_on("boost+regex+program_options+filesystem+system+test")
    depends_on("cetlib-except")
    depends_on("hep-concurrency", when="@3.18.01:", type=("build", "test"))
    depends_on("hep-concurrency", when="@:3.18.00")
    with when("@3.14.00:"):
        if sys.platform != "darwin":
            depends_on("openssl")
    depends_on("openssl", when="@:3.13")
    depends_on("perl", type=("build", "run"))
    depends_on("sqlite@3.8.2:")
    depends_on("catch2@3.3.0:", when="@3.17:", type=("build", "test"))
    depends_on("catch2@2.3.0:2", when="@:3.16", type=("build", "test"))
    depends_on("cetmodules", type="build")
    conflicts("cetmodules@:3.21.00", when="catch2@3:")
    # TBB is an indirect dependency (from hep-concurrency) required
    # explicitly for unknown reasons.
    depends_on("tbb", type=("build", "test"))

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
        # Binaries required for some of the tests.
        env.prepend_path("PATH", prefix.bin)
        # For plugin tests (not needed for installed package).
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Perl modules.
        env.prepend_path("PERL5LIB", prefix.perllib)

    @sanitize_paths
    def setup_run_environment(self, env):
        # Perl modules.
        env.prepend_path("PERL5LIB", self.prefix.perllib)

    @sanitize_paths
    def setup_dependent_build_environment(self, env, dependent_spec):
        # Perl modules.
        env.prepend_path("PERL5LIB", self.prefix.perllib)
