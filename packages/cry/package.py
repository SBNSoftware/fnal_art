# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob
import os
import sys

from spack.package import *

libdir = "%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if libdir not in sys.path:
    sys.path.append(libdir)


def patcher(x):
    cetmodules_20_migrator(".", "cry", "1.7")


class Cry(MakefilePackage):
    """Generates correlated cosmic-ray particle showers at one of three
    elevations (sea level, 2100m, and 11300m) for use as input to transport
    and detector simulation codes."""

    homepage = "https://nuclear.llnl.gov/simulation/"
    url = "https://nuclear.llnl.gov/simulation/cry_v1.7.tar.gz"

    version("1.7", sha256="dcee2428f81cba113f82e0c7c42f4d85bff4b8530e5ab5c82c059bed3e570c20")

    parallel = False

    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    @run_before("build")
    def filter_makefile(self):
        makefile = FileFilter("Makefile.common")
        makefile.filter("CXX = .*", "")
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        with open("Makefile.local", "w") as f:
            f.write("CXXFLAGS += -O3 -g -DNDEBUG -fno-omit-frame-pointer -fPIC \\\n")
            f.write("            {0}\n".format(cxxstdflag))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            for f in glob.glob("src/*.o"):
                os.remove(f)
            setup = FileFilter("setup")
            setup.filter('^cd ".*', 'cd "%s"' % prefix)
            install_tree(self.stage.source_path, prefix)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("CRYHOME", self.prefix)
        spack_env.set("CRY_LIB", self.prefix.lib)
        spack_env.set("CRYDATAPATH", self.prefix.data)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.src)

    def setup_run_environment(self, run_env):
        run_env.set("CRYHOME", self.prefix)
        run_env.set("CRY_LIB", self.prefix.lib)
        run_env.set("CRYDATAPATH", self.prefix.data)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.src)

    @run_after("install")
    def rename_README(self):
        import os

        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename(
                join_path(self.spec.prefix, "README"),
                join_path(self.spec.prefix, "README_%s" % self.spec.name),
            )
