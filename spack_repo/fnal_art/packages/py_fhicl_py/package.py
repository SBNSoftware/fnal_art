# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class PyFhiclPy(CMakePackage, FnalGithubPackage):
    """Python bindings for the FHiCL configuration language."""

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/fhicl-py"

    version_patterns = ["v4_04_04"]

    maintainers("gartung", "greenc-FNAL", "knoepfel", "marcmengel", "marcpaterno")

    license("BSD-3-Clause", checked_by="greenc-FNAL")

    version("develop", branch="develop", get_full_repo=True)
    version("4_04_00", sha256="336894eb70cdb7e60fa22d05f97d99a2d994ac4c44b9763d06a0af2ca9b908a6")

    cxxstd_variant("17", "20", "23", default="20", sticky=True)

    extends("python")
    depends_on("cxx", type="build")
    depends_on("cetmodules@3.19.02:", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("py-pybind11", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
