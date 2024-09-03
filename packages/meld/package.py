# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Meld(CMakePackage, FnalGithubPackage):
    """A project for exploring how to meet DUNE's framework needs."""

    repo = "knoepfel/meld.git"
    version_patterns = []

    maintainers("knoepfel")

    license("Apache-2.0")

    version("develop", branch="main", get_full_repo=True)

    cxxstd_variant("20", "23", default="20", sticky=True)

    depends_on("boost@1.75.0: +json+program_options+stacktrace")
    depends_on("fmt@:9")
    depends_on("jsonnet")
    depends_on("spdlog")
    depends_on("tbb")
    depends_on("libbacktrace +shared")
    depends_on("catch2", type=("build", "test"))

    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")
        ]
