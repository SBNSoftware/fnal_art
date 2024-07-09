# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Marley(Package):
    """A Monte Carlo event generator for tens-of-MeV neutrino-nucleus
    interactions in liquid argon"""

    homepage = "httpd://github.com/sjgardiner/marley"
    url = "https://github.com/MARLEY-MC/marley/archive/v1.2.1.tar.gz"

    version("1.2.1", sha256="75e8e4acbbcf7ad9de0ef629ac9e8764ebf90fda2242ff5e6e590e77f9df6972")
    version("1.2.0", sha256="8bb0a68924c8e5d7773904151e3134c6c59837723ecf4e1b586a6cb5b48b520d")
    version("1.0.0", sha256="4dea9918cff0aed3b9c38f74351c373c32235496ca6e321078f2c7b56bce719e")
    version("1.1.0", sha256="04d484468d08e5447dfd2fde20bea5bbebfd04ecb6eb34ad65b30f3825bcd577")
    version("1.1.1", sha256="214f8a40e59d47dd563be53640c5f197f5529bcb0ee65a9402cca450a611c0f8")
    version("1.2.0", sha256="8bb0a68924c8e5d7773904151e3134c6c59837723ecf4e1b586a6cb5b48b520d")

    variant(
        "cxxstd",
        default="17",
        values=("98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("root")
    depends_on("gsl")

    patch("marley-1.0.0.patch", when="@1.0.0")
    patch("marley-1.1.0.patch", when="@1.1.0")
    patch("marley-1.1.1.patch", when="@1.1.1")
    patch("marley-1.2.0.patch", when="@1.2.0")
    patch("marley-1.2.1.patch", when="@1.2.1")

    def patch(self):
        cxxstd = self.spec.variants["cxxstd"].value
        filter_file("CXX_STD=c\+\+14", f"CXX_STD=c\+\+{cxxstd}", "build/Makefile")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.append_flags("CPPFLAGS", "-I../include")
        cxxstd_flag = "cxx{0}_flag".format(self.spec.variants["cxxstd"].value)
        spack_env.append_flags("CXXFLAGS", getattr(self.compiler, cxxstd_flag))

    def install(self, spec, prefix):
        with working_dir("build"):
            make("prefix={0}".format(prefix), "install")

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FW_SEARCH_PATH", self.prefix.share.data)
        run_env.append_path("FW_SEARCH_PATH", self.prefix.share.data.react)
        run_env.append_path("FW_SEARCH_PATH", self.prefix.share.data.structure)
