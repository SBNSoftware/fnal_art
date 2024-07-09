# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Art(CMakePackage, FnalGithubPackage):
    """The eponymous package of the art suite; art is an event-processing
    framework for particle physics experiments.
    """

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/art"

    version_patterns = ["v3_04_00"]

    version("3.15.00", sha256="3faa8c90d85b5ac100c56584f2bf05a664ed6d5243e53df1fe9e4372d4136eed")
    version("3.14.04", sha256="2b930299e1f3fe52544fe0a8f7beaba614c1aea56efe832fffb7117f497e110c")
    version("3.14.03", sha256="c16b8b69a540fe00090e56ff6911c356615dd2c82179d57373024bcb01984434")
    version("3.14.02", sha256="8cc7340a1a92ee22ddeacc3b1ad8a0688561d4fb2a790f42be791534bce8ea2e")
    version("3.14.01", sha256="29489e0dc7abf2756c9081569a54dbb49c8cbb472c651e343d6ce2d49fc1cac2")
    version("3.14.00", sha256="20eaa43d68b07eb5ea87c10c2e1b85a91dc5eaa3b4b83841b67e76dd64399ef0")
    version("3.13.02", sha256="c0a39ef326daee1e77cfb73d56ea08533be0e8d281e9e937814e258622758158")
    version("3.13.01", sha256="bb81d781f2e6e6bd223c9008c8b36b9dc6ed0138e173325f2ef218c798017258")
    version("3.12.00", sha256="d47c6fb30f5b5c93fe8ceea495e245c294bbc8166fcaccbd314d535fe12eb059")
    version("3.11.00", sha256="4c3076577de227c705f2ba057abcc3923f37c9b4d5a2165fbc0536598e0f671a")
    version("3.10.00", sha256="128fccc84c7a953ed0a0a28c6cdee86299851dbe402f78e7f1230501cc23e1e4")
    version("3.09.04", sha256="01a3f88f0c4b179dcfe8492ea356832df23bf974d35faa1c1d6f220789768e4f")
    version("3.09.03", sha256="f185fecd5593217185d2852d2ecf0a818326e7b4784180237461316b1c11f60d")
    version("3.09.00", sha256="d2a49e529da4f744df0fc3f9be9e44a908dbedd08fcdcd4e2e9ba2e08521c1b2")
    version("3.05.00", sha256="3f307b4fdaf113388d49e603cb29eeb99f5f0f3fd1186f0a9950e7ab793baa90")
    version("3.04.00", sha256="38d27e1776adad157ad2d4e8c073ecda67ec4677fff9ebbffef6e37d7ed1d8ff")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@3.15.00:")

    depends_on("boost@:1.82", when="@:3.15")
    depends_on("boost+date_time+graph+program_options+regex")
    depends_on("boost@1.75: +filesystem+json+test+thread", type=("build"))
    depends_on("boost+graph+test", type=("test"))
    depends_on("canvas")
    depends_on("catch2@2.3.0", type=("build", "test"), when="@:3.11.99")
    depends_on("catch2@3:", type=("build", "test"), when="@3.12:")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules", type="build")
    conflicts("cetmodules@:3.21.00", when="catch2@3:")
    depends_on("clhep")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency")
    depends_on("messagefacility")
    depends_on("perl")
    depends_on("range-v3@0.11.0:", type="build")
    depends_on("sqlite@3.8.2:")
    depends_on("tbb")

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
    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
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
