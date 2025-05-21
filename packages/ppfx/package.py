# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ppfx(CMakePackage):
    """Package to Predict the FluX"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ppfx"
    homepage_soon = "https://github.com/kordosky/ppfx"
    git = "https://cdcvs.fnal.gov/redmine/projects/ppfx"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/ppfx.v02_18_03.tbz2"
    url_soon = "https://github.com/kordosky/ppfx/archive/tag/v02.13.03.tar.gz"

    maintainers = ["marcmengel", "kordosky"]

    def url_for_version(self, version):
        urlf = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/ppfx.v{0}.tbz2"
        return urlf.format(version.underscored)

    version("02.18.03", sha256="32bab85a7d98b06ecfd76fe57df28cef7fb826ab8fd89ab1bb56f34ab8260040")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("doxygen", type="build")
    depends_on("nufinder", type="build")

    depends_on("art")
    depends_on("boost")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetbuildtools")
    depends_on("cry")
    depends_on("dk2nudata")
    depends_on("dk2nugenie")
    depends_on("fftw")
    depends_on("genie")
    depends_on("ifdh-art")
    depends_on("ifdhc")
    depends_on("lhapdf")
    depends_on("libwda")
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("nusimdata")
    depends_on("postgresql")
    depends_on("pythia6")
    depends_on("root")
    depends_on("xerces-c")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"), "-Dppfx_FW_DIR=fw"]
        return args

    def setup_build_environment(self, env):
        env.set("CANVAS_ROOT_IO_DIR", self.spec["canvas"].prefix)
        env.set("CETBUILDTOOLS_DIR", self.spec["cetbuildtools"].prefix)
        env.set("CRYHOME", self.spec["cry"].prefix)
        env.set("DK2NUDATA_LIB", self.spec["dk2nudata"].prefix)
        env.set("DK2NUGENIE_INC", self.spec["dk2nugenie"].prefix)
        env.set("GENIE_INC", self.spec["genie"].prefix)
        env.set("GENIE_LIB", self.spec["genie"].prefix)
        env.set("IFDH_ART_FQ_DIR", self.spec["ifdh-art"].prefix)
        env.set("IFDH_ART_LIB", self.spec["ifdh-art"].prefix)
        env.set("IFDHC_FQ_DIR", self.spec["ifdhc"].prefix)
        env.set("IFDHC_LIB", self.spec["ifdhc"].prefix)
        env.set("LHAPDF_LIB", self.spec["lhapdf"].prefix)
        env.set("LIBXML2_INC", self.spec["libxml2"].prefix)
        env.set("LOG4CPP_INC", self.spec["log4cpp"].prefix)
        env.set("LOG4CPP_LIB", self.spec["log4cpp"].prefix)
        env.set("PYLIB", self.spec["pythia6"].prefix)
        env.set("XERCES_C_INC", self.spec["xerces-c"].prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FW_SEARCH_PATH", "{0}/fw".format(self.prefix))
        run_env.append_path("CET_PLUGIN_PATH", self.prefix.lib)

