# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ifbeam(MakefilePackage):
    """Data handling client code for intensity frontier experiments"""

    homepage = "https://github.com/fnal-fife/ifbeam"
    git_base = "https://github.com/fnal-fife/ifbeam.git"
    url = "https://github.com/fnal-fife/ifbeam/archive/refs/tags/v2_6_2.tar.gz"
    list_url = "https://github.com/fnal-fife/ifbeam/tags"

    version("2.6.3", sha256="1a0d2cc50ef73d459b3d8e29e712606b9f5ef9c8e84dc06a50a809b1cc829128")
    version("2.6.2", sha256="8297ecab83e215661097f786b88d1e1f03a50299780ff5862bf674b382288325")
    version("2.6.1", sha256="1fc548013803f2cd9c9c93fb526e6efc3519634edff07a0455019d78cc96a77e")
    version("2.6", sha256="c156a2ba05e7b6f376b678bd53dbca53558f7127ac5bbe32083a648eeb10f1c2")
    version("2.5.23", sha256="a0b4890045cf5efdb4f19183dd417a1f5fdfc82d62f44d989b21a55210b9aef6")
    version("2.5.22", sha256="648246ab995b16e5da7f95b1e63c1520d71cf91af942fc8e96f4fed24fae85ff")
    version("2.5.21", sha256="26b8abf691738a29256e14a14b1cfa50fdd709cf2462b87601cb3fa7e6d1c83d")
    version("2.5.20", sha256="fe29c9b60a169390ab58205c3859099a1636d866af545c6e6fd315b11f11f2e7")
    version("2.5.19", sha256="8b47f7011253d1686a31336cd3549d1e4675ad987750273d500bbeb14cf5ff22")
    version("2.5.18", sha256="fa10d65522b744b0230cb7bdc103a01f4248428a12a98510ec1c15d9cf81c51a")

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
    depends_on("libwda")

    def patch(self):
        filter_file(r'catch \(WebAPIException e\)','catch (WebAPIException &e)','src/ifbeam.cc') 

    def url_for_version(self, version):
        url = "https://github.com/fnal-fife/ifbeam/archive/refs/tags/v{0}.tar.gz"
        return url.format("ifdhc-" + self.name, version.underscored)

    @property
    def build_targets(self):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        tlist = [
            "LIBWDA_FQ_DIR=" + self.spec["libwda"].prefix,
            "LIBWDA_LIB=" + self.spec["libwda"].prefix.lib,
            "IFDHC_FQ_DIR=" + self.spec["ifdhc"].prefix,
            "IFDHC_LIB=" + self.spec["ifdhc"].prefix.lib,
            "ARCH=" + cxxstdflag,
        ]

        if "ubuntu" in self.spec.architecture:
            tlist.append("LDFLAGS=-lcrypto")

        return tlist

    @property
    def install_targets(self):
        return ("DESTDIR={0}/".format(self.prefix), "install")

    def setup_build_environment(self, spack_env):
        spack_env.set("IFBEAM_DIR", self.prefix)

    def setup_run_unvironment(self, run_env):
        run_env.set("IFBEAM_DIR", self.prefix)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("IFBEAM_DIR", self.prefix)

    def setup_run_environment(self, run_env):
        run_env.set("IFBEAM_DIR", self.prefix)
