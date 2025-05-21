# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *

libdir = "%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if libdir not in sys.path:
    sys.path.append(libdir)


def patcher(x):
    cetmodules_20_migrator(".", "artg4tk", "9.07.01")


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Icarusutil(CMakePackage):
    """icarusutil"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/icarusutil"
    url = "https://cdcvs.fnal.gov/projects/icarusutil"
    git_base = "https://github.com/SBNSoftware/icarusutil.git"

    version("08.36.00", tag="v08_36_00", git=git_base, get_full_repo=True)
    version("08.39.00", tag="v08_39_00", git=git_base, get_full_repo=True)
    version("08.41.00", tag="v08_41_00", git=git_base, get_full_repo=True)
    version("08.43.00", tag="v08_43_00", git=git_base, get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("art-root-io")
    depends_on("larbatch")
    depends_on("py-pycurl")
    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build")

    patch("cetmodules2.patch")

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        spack_env.prepend_path("PYTHONPATH", os.path.join(self.build_directory, "bin"))
        spack_env.prepend_path("PYTHONPATH", os.path.join(self.build_directory, "python"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        # Perl modules.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("ICARUSUTIL_INC", self.prefix.include)
        spack_env.set("ICARUSUTIL_LIB", self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
