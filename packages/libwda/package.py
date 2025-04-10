# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libwda(MakefilePackage):
    """Fermilab Web Data Access library"""

    homepage = "https://github.com/fnal-fife/libwda"
    git_base = "https://github.com/fnal-fife/libwda.git"
    url = "https://github.com/fnal-fife/libwda/archive/refs/tags/v2_6_14.tar.gz"
    list_url = "https://github.com/fnal-fife/libwda/tags"

    version("2.30.0", sha256="ace33ae85cd418d37ad882ab38a0ce76397a65ae6f9a5d229707a06e62bf5204")
    version("2.29.1", tag="v2_29_1", git=git_base, get_full_repo=True)
    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("2.26.0", sha256="4df374bbf36030241a9714d5e08cd9b2b5e1b3374da1a97ec793cd37eba40fc2")
    version("2.22.2", tag="v2_22_2", git=git_base, get_full_repo=True)
    version("2.23.0", tag="v2_23_0", git=git_base, get_full_repo=True)
    version("2.24.0", tag="v2_24_0", git=git_base, get_full_repo=True)
    version("2.26.0", tag="v2_26_0", git=git_base, get_full_repo=True)

    parallel = False

    build_directory = "src"

    depends_on("curl")
    depends_on("zlib")
    depends_on("openssl")
    depends_on("pcre")

    patch("version.patch", level=1)

    @property
    def build_targets(self):
        tlist = [
            "LIBWDA_VERSION=v{0}".format(self.version.underscored),
            "LDFLAGS=-lcrypto", # rather than bigger Makefile patch
        ]
        return tlist

    @property
    def install_targets(self):
        return ("PREFIX={0}".format(prefix), "install")

    def url_for_version(self, version):
        url = "https://github.com/fnal-fife/libwda/archive/refs/tags/v{0}.tar.gz"
        return url.format("-".join(("ifdhc", self.name)), version.underscored)

    @run_before("build")
    def filter_makefile(self):
        makefile = FileFilter(os.path.join("src", "Makefile"))
        makefile.filter("gcc", "$(CC)")

    def setup_build_environment(self, spack_env):
        spack_env.set("LIBWDA_DIR", self.prefix)

    def setup_run_environment(self, run_env):
        run_env.set("LIBWDA_DIR", self.prefix)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LIBWDA_DIR", self.prefix)
        spack_env.set("LIBWDA_LIB", self.prefix.lib)
        spack_env.set("LIBWDA_INC", self.prefix.include)
