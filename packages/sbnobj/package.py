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


class Sbnobj(CMakePackage):
    """The eponymous package of the Sbn experiment
    framework for particle physics experiments.
    """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/sbnobj"
    git_base = "https://cdcvs.fnal.gov/projects/sbnobj"
    git_base = "https://github.com/SBNSoftware/sbnobj.git"

    version(
        "develop",
        commit="821c5e24aa509b4e1ba0eda064d3ce5f3fbce1a2",
        git=git_base,
        get_full_repo=True,
    )
    version("09.12.12", sha256="60f4f1d437cad1b1573c5f56186a48edbeab1431ccdeb0bcbe8d62fc3c7b21b0")
    version("09.12.09", sha256="4905f82711ac35fcdb732500ce1a33cee83f38a66a116d3d30aeeca749ba1313")
    version("09.12.05", tag="v09_12_05", git=git_base, get_full_repo=True)
    version("09.12.04", tag="v09_12_04", git=git_base, get_full_repo=True)
    version("09.09.00", tag="v09_09_00", git=git_base, get_full_repo=True)
    version("09.09.01", tag="v09_09_01", git=git_base, get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("v09_12_12.patch", when="@09.12.12")
    patch("v09_12_09.patch", when="@09.12.09")
    patch("v09_12_05.patch", when="@09.12.05")
    patch("v09_12_04.patch", when="@09.12.04")
    patch("cetmodules2.patch", when="@develop")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Build-only dependencies.
    depends_on("cmake@3.11:")
    depends_on("cetmodules", type="build")

    # Build and link dependencies.
    depends_on("artdaq-core", type=("build", "run"))
    depends_on("art-root-io", type=("build", "run"))
    depends_on("art", type=("build", "run"))
    depends_on("artdaq-core", type=("build", "run"))
    depends_on("boost", type=("build", "run"))
    depends_on("canvas-root-io", type=("build", "run"))
    depends_on("canvas", type=("build", "run"))
    depends_on("cetlib", type=("build", "run"))
    depends_on("cetlib-except", type=("build", "run"))
    depends_on("clhep", type=("build", "run"))
    depends_on("cppgsl", type=("build", "run"))
    depends_on("eigen", type=("build", "run"))
    depends_on("fhicl-cpp", type=("build", "run"))
    depends_on("fftw", type=("build", "run"))
    depends_on("hep-concurrency", type=("build", "run"))
    depends_on("ifdh-art", type=("build", "run"))
    depends_on("tbb", type=("build", "run"))
    depends_on("geant4", type=("build", "run"))
    depends_on("larana", type=("build", "run"))
    depends_on("larcoreobj", type=("build", "run"))
    depends_on("larcorealg", type=("build", "run"))
    depends_on("larcore", type=("build", "run"))
    depends_on("lardataobj", type=("build", "run"))
    depends_on("lardataalg", type=("build", "run"))
    depends_on("lardata", type=("build", "run"))
    depends_on("larevt", type=("build", "run"))
    depends_on("larpandora", type=("build", "run"))
    depends_on("larpandoracontent", type=("build", "run"))
    depends_on("larreco", type=("build", "run"))
    depends_on("larsim", type=("build", "run"))
    depends_on("libwda", type=("build", "run"))
    depends_on("marley", type=("build", "run"))
    depends_on("messagefacility", type=("build", "run"))
    depends_on("nug4", type=("build", "run"))
    depends_on("nusimdata", type=("build", "run"))
    depends_on("dk2nudata", type=("build", "run"))
    depends_on("nutools", type=("build", "run"))
    depends_on("postgresql", type=("build", "run"))
    depends_on("root", type=("build", "run"))
    depends_on("range-v3", type=("build", "run"))
    depends_on("sbndaq-artdaq-core", type=("build", "run"))
    depends_on("sqlite", type=("build", "run"))
    depends_on("trace", type=("build", "run"))
    depends_on("py-srproxy", type=("build", "run"))

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def url_for_version(self, version):
        # url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args.
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)

        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", os.path.join(self.prefix, "bin"))
        # Ensure we can find plugin libraries.
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
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleanup.
        sanitize_environments(spack_env)
