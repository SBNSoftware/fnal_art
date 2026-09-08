# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Canvas(CMakePackage, FnalGithubPackage):
    """The underpinnings for the art suite."""

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/canvas"

    version_patterns = ["v3_12_04"]

    version("3.17.00", sha256="05c08194b49e5467bffbd89dc99d2b7ec357c8ae021445b32a190509a9bb60dc")
    version("3.16.04", sha256="11278f758e40e96f1d1ffad61625e4bfc6067e0623cd191c6c8227c265e2c44f")
    version("3.16.03", sha256="150f82d37c402b4e428b040f047ef9e2b9613a8d8d8803aba03137a754bb7a47")
    version("3.16.01", sha256="e8eb606d38dfa8d5c56cf6074212e83cbf55de80c3bff51b1167704d9adb4169")
    version("3.15.02", sha256="7569ce0c2f64f2932b2c6d2e6a734e45d7ca21af652e0192b4f216373870ec24")
    version("3.15.01", sha256="7a2b839f5c564c1a9d719203c4bb68b2feb95019c9e2a92bf30302adbba09047")
    version("3.14.00", sha256="f3dd81aa1770c62e3329409a3849db13c7b7818d4927a52ceb82f5e7f3f0ebf4")
    version("3.13.01", sha256="ad84161ad37b30675664994ba37a8f4ee5001d5936ebabc24b79b9a3c9419515")
    version("3.13.00", sha256="6d5d6d817907fada8504514d5c9009f6b48a7afd606fa4bed3793d30aad347b7")
    version("3.12.05", sha256="e0a0506528ab1f4db4b76bd3b68f0ea1ea97a627a68930abbfa1b2bfea069ee9")
    version("3.12.04", sha256="bcbb9680000a0f1eec4ec3983b49d8a89f6820d4abdee2ffcb7bd769a0799974")

    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", "23", default="17", sticky=True)

    depends_on("boost+date_time+test")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules", type="build")
    depends_on("clhep")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("catch2", type=("build", "test"))
    depends_on("hep-concurrency", type=("build", "test"))
    depends_on("messagefacility")
    depends_on("range-v3@0.11:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        # Binaries.
        env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
