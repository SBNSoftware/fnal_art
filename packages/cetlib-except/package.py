# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class CetlibExcept(CMakePackage, FnalGithubPackage):
    """Exception libraries for the art suite."""

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/cetlib-except"

    version_patterns = ["v1_07_04"]

    version("1.10.00", sha256="69960e18e80ee76ce7437366d3d916e653ced32aae0365362750d8226e51f87b")
    version("1.09.01", sha256="72ed76819ce98c1629e55931a939374d386070b77070b849e029d095097240fd")
    version("1.09.00", sha256="49d28d96fe2ae96aeb1c636b356e731dda60c4b69b0c7759de484225f4e4a380")
    version("1.08.00", sha256="2951be7cd7b58c05c09a89fdd8b2b287262447d7e69e13bef7a15a98040d4efd")
    version("1.07.06", sha256="49324dcd254dcd1183715d4bb6ea5ccf394231e717ebb4c08cf0ab0c1d976bdf")
    version("1.07.04", sha256="d021d26fda9f4f57b57850bc6f5ac0a79aed913ef1cde68a96838ad85d332d70")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@1.10.00:")

    depends_on("catch2@2.3.0:2", when="@:1.08", type=("build", "test"))
    depends_on("catch2@3.3.0:", when="@1.09:", type=("build", "test"))
    depends_on("cetmodules@3.19.02:", type="build")
    conflicts("cetmodules@:3.21.00", when="catch2@3:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        # For tests.
        env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
