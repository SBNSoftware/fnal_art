# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Artg4(CMakePackage):
    """Generic geant4 infrastructure for Art"""

    homepage = "https://cdcvs.fnal.gov/projects/artg4/wiki"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/artg4.v9_70_00.tbz2"

    maintainers = ["marcmengel"]

    variant("cxxstd", default="17")

    version("9.70.00", sha256="f77c5afac341562451127ebe7657844049a1fb8c860850638fff32641ffce2e6")

    def patch(self):
        filter_file(
            "^CMAKE_MINIMUM_REQUIRED.*",
            "CMAKE_MINIMUM_REQUIRED( VERSION 3.14 )\nfind_package(cetmodules)",
            "CMakeLists.txt",
        )
        filter_file(
            "^PROJECT.*",
            "PROJECT({0} VERSION {1} LANGUAGES CXX C)".format(self.name, self.version),
            "CMakeLists.txt",
        )
        filter_file(r"add_subdirectory\(ups\)", "if(WANT_UPS)\n\nendif()", "CMakeLists.txt")

    def url_for_version(self, version):

        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"
        # url = 'https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    variant("cxxstd", default="17")

    depends_on("cetbuildtools", type=("build"))
    depends_on("cetmodules", type=("build"))
    depends_on("boost", type=("build","run"))
    depends_on("intel-tbb-oneapi", type=("build","run"))
    depends_on("cetpkgsupport", type=("build", "run"))
    depends_on("art", type=("build", "run"))
    depends_on("canvas", type=("build", "run"))
    depends_on("canvas-root-io", type=("build", "run"))
    depends_on("geant4", type=("build", "run"))
    depends_on("xerces-c", type=("build", "run"))
    depends_on("fhicl-cpp", type=("build", "run"))
    depends_on("messagefacility", type=("build", "run"))


    def cmake_args(self):
        args = [
            "-DCXX_STANDARD=%s" % self.spec.variants["cxxstd"].value,
            "-DOLD_STYLE_CONFIG_VARS=True",
            "-DCMAKE_MODULE_PATH={0}".format(
                          self.spec['cetmodules'].prefix.Modules.compat),
            "-DUPS_PRODUCT_VERSION=v{0}".format(self.spec.version.underscored),
        ]
        return args

    def setup_build_environment(self, env):
        # set environment variables used in CMakeLists.txt
        env.set("CETBUILDTOOLS_VERSION", self.spec['cetbuildtools'].version)
        env.set("CANVAS_ROOT_IO_DIR", self.spec['canvas-root-io'].prefix)

