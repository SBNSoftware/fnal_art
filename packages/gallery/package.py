# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Gallery(CMakePackage, FnalGithubPackage):
    """A library to allow reading of Root output files produced by the art
    suite.
    """

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/gallery"

    version_patterns = ["v1_20_02"]

    version("develop", branch="develop", get_full_repo=True)
    version("1.23.00", sha256="610a01297a1c7b3509989084a34903714ce23cb052a71d54f9a2afff7547f2e8")
    version("1.22.06", sha256="d92203e49703e1c97acb9865e3d90c77045dbbf8f6dcedf76d1e68f9ee3bf719")
    version("1.22.05", sha256="0aaee9c0473fcc6ee2588f8a552b64616ef5c32e6ad38b48548efa00c807001b")
    version("1.22.03", sha256="a215a89933500082e8ddd1a6bcfc5c01c4f07c041b552788364868cfc2baa004")
    version("1.22.01", sha256="86dd9bbc88f765e1b7ea75b49e6f3af401b9f92461e91bd9d65b407bad5a14cb")
    version("1.21.01", sha256="e932c2469de4abb87527defe7357ea6423e8dbc18ef9d9b5148e5e658c3ffc91")
    version("1.21.02", sha256="0eb3eff1a173d09b698e1ba174ab61d9af72937067b300f1b73d0eca73349294")
    version("1.21.03", sha256="b1f41e1e4efcaf73b6c90c12dc513217ea5591ce369a9335d2ca6f4d0f2b1728")
    version("1.20.02", sha256="433e2b5727b9d9cf47206d9a01db5eab27c5cbb76407bb0ec14c0fd4e4dc41f9")

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@1.23.00:")

    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetmodules", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("range-v3", type=("build", "link", "run"))
    depends_on("root+python")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
