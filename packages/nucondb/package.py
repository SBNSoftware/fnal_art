# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nucondb(MakefilePackage):
    """Data handling client code for intensity frontier experiments"""

    homepage = "https://github.com/fnal-fife/nucondb"
    git_base = "https://github.com/fnal-fife/nucondb.git"
    url = "https://github.com/fnal-fife/nucondb/archive/refs/tags/v2_6_14.tar.gz"
    list_url = "https://github.com/fnal-fife/nucondb/tags"

    version("2_6_2", sha256="3fffd0d4291c76dbba0f94c75d678057ae12d1a36983c8cccd7098158f7b6874")
    version("2_6_1", sha256="0fd793361322224c74c413dc105fb53f60488a6234c5ad4f31843e6b4462d39e")
    version("2_6", sha256="e205a12c28466bdf32ec4373a76877e28606f6ed33f58d1d64c738ac03d232d7")
    version("2_5_23", sha256="eb8c0b9720ffcc0e2146ee704349f7ce41748ca91614aeb9644ec388c4f7ad4d")
    version("2_5_22", sha256="583917373cedce05150d892541402332795444ec019d961870807150da540079")
    version("2_5_21", sha256="20c19e30ac6eda4df5058d2ca6753ad6c0de25c80df495b5fa97910966af7140")
    version("2_5_20", sha256="1395d43c3bb954bf0982b85a1f49ee6a9454924f2d403f74a35be75c19f101c9")
    version("2_5_19", sha256="73d589ba9437c40e990c7b872f8ff5154e32697f9e1990d6253d898ed11b810f")
    version("2_5_18", sha256="f1ed5f66aa373292eb917d09885f2f2fbc41385521fb396050d441e300508f2a")
    version("2.5.2", tag="v2_5_2", get_full_repo=True)
    version("2.4.8", tag="v2_4_8", get_full_repo=True)
    version("2.3.0", tag="v2_3_0", get_full_repo=True)
    version("2.2.10", tag="v2_2_10", get_full_repo=True)

    parallel = False

    build_directory = "src"

    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("ifdhc")
    depends_on("ifbeam")
    depends_on("libwda")

    def patch(self):
        filter_file(
            r"catch \(WebAPIException we\)", "catch (WebAPIException &we)", "src/nucondb.cc"
        )

    @property
    def build_targets(self):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        return [
            "LIBWDA_FQ_DIR=" + self.spec["libwda"].prefix,
            "LIBWDA_LIB=" + self.spec["libwda"].prefix.lib,
            "IFDHC_FQ_DIR=" + self.spec["ifdhc"].prefix,
            "IFBEAM_FQ_DIR=" + self.spec["ifbeam"].prefix,
            "IFDHC_LIB=" + self.spec["ifdhc"].prefix.lib,
            "ARCH=" + cxxstdflag,
        ]

    @property
    def install_targets(self):
        return ("DESTDIR={0}/".format(self.prefix), "install")

    def setup_build_environment(self, spack_env):
        spack_env.set("NUCONDB_DIR", self.prefix)

    def setup_run_environment(self, run_env):
        run_env.set("NUCONDB_DIR", self.prefix)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("NUCONDB_DIR", self.prefix)
