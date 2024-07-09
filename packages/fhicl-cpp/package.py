# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class FhiclCpp(CMakePackage, FnalGithubPackage):
    """A C++ implementation of the FHiCL configuration language for the art
    suite.
    """

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/fhicl-cpp"

    version_patterns = ["v4_15_03"]

    version("4.19.00", sha256="25163d17a9a6c8509d326785a78e399fdc33e231ad393edc0ae34b1d9b56b9f9")
    version("4.18.04", sha256="d0b8beca890707d0bbf35678c3b6bddd1b02b3ab7654801abbe31525dacdd7b5")
    version("4.18.03", sha256="c08fd6ce37225e58d3d893f9205b321ae2fff2d8b5c96c2e22ac24708a4309af")
    version("4.18.02", sha256="ca96ed2f524061b0b9c03aef50d9ef9aad1295d331195e07f7584da7b63ba946")
    version("4.18.01", sha256="ad99cdf48b912fc51852229e04896c04db6db55a7c49f873156dae6665d8bfa7")
    version("4.18.00", sha256="cd5c7c0bef5e235264bf22819db283bd3ebfd512ecab06fb3722142cec0a0a5e")
    version("4.17.00", sha256="07fbba4aed129fcc5edbd9a7304dc3ccd53d2405830779e7c2d71a8b73a99247")
    version("4.15.03", sha256="99ae2b7557c671d0207dea96529e7c0fca2274974b6609cc7c6bf7e8d04bd12b")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@4.19.00:")

    depends_on("boost@:1.82", when="@:4.19")
    depends_on("boost+program_options+test")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules@3.19.02:", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("hep-concurrency", type="build")
    depends_on("openssl")
    depends_on("py-pybind11", type="build")
    depends_on("python")
    depends_on("sqlite")
    depends_on("tbb")

    patch("test_build.patch", when="@:4.17.00")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        # Path for tests.
        env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))

    @sanitize_paths
    def setup_run_environment(self, env):
        # Bash completions.
        bindir = self.prefix.bin
        env.from_sourcing_file(os.path.join(bindir, "fhicl-dump_completions"))
        env.from_sourcing_file(os.path.join(bindir, "fhicl-expand_completions"))
        env.from_sourcing_file(os.path.join(bindir, "fhicl-get_completions"))
