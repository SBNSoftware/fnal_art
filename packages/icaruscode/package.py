# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *
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


class Icaruscode(CMakePackage):
    """The eponymous package of the Icarus experiment
    framework for particle physics experiments.
    """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/icaruscode"
    git_base = "https://github.com/SBNSoftware/icaruscode.git"

    version(
        "develop",
        commit="84314472f1e206b351fd9b52f1f6800c2a90b4c3",
        git=git_base,
        get_full_repo=True,
    )

    version("10.06.00.01p04", sha256="4ae01238f61b326feb9d58d1b4a33c7ad8f42054ad661d012b6041bd72288c3e")
    version("10.06.00.01", sha256="03c7d0f86e0247e04acc0f58c57c85d1ab735f65df8b375966bcb1135a0da22a")
    version("10.04.04", sha256="0b59e6ee4b1c04a6d146514a4e574882bf70de4c8956d08e357e2dee4de595e5")
    version("09.91.02.01", "77048becd1a960b9e4e19e110d05fca135457b224507f9feaada8d98d2f1cc2b")
    version(
        "09.37.02.03", sha256="1762e5a05ebac100032b2bc46244a63f3bc454f51a583da03b935a6827d7df6f"
    )
    version("09.37.01.03p02", tag="v09_37_01_03p02", git=git_base, get_full_repo=True)
    version("09.37.01.vec03p02", tag="v09_37_01_03p02", git=git_base, get_full_repo=True)
    version("09.37.01.02p02", tag="v09_37_01_02p02", git=git_base, get_full_repo=True)
    version("09.37.01.vec02p02", tag="v09_37_01_02p02", git=git_base, get_full_repo=True)
    version("09.35.00", tag="v09_35_00", git=git_base, get_full_repo=True)
    version("08.43.00", tag="v08_43_00", git=git_base, get_full_repo=True)
    version("08.41.00", tag="v08_41_00", git=git_base, get_full_repo=True)
    version("08.40.00", tag="v08_40_00", git=git_base, get_full_repo=True)
    version("08.39.00", tag="v08_39_00", git=git_base, get_full_repo=True)
    version("08.50.00", tag="v08_50_00", git=git_base, get_full_repo=True)
    version("08.50.02", tag="v08_50_02", git=git_base, get_full_repo=True)

    patch("cetmodules2.patch", when="@develop")
    patch("v09_35_00.patch", when="@09.35.00")
    patch("v09_91_02_01.patch", when="@09.91.02.01")
    patch("v09_37_01_03p02.patch", when="@09.37.01.03p02")
    patch("v09_37_01_02p02.patch", when="@09.37.01.02p02")
    patch("v09_37_01_02p02_larvecutils.patch", when="@09.37.01.vec02p02")
    patch("v09_37_01_03p02_larvecutils.patch", when="@09.37.01.vec03p02")
    patch("v09_37_02_03.patch", when="@09.37.02.03")
    patch("spack.patch")

    def patch(self):
        filter_file('find_package\(icarusutil REQUIRED \)','','CMakeLists.txt')

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # Build-only dependencies.
    depends_on("cmake@3.11:")
    depends_on("cetmodules", type="build")

    # Build and link dependencies.
    depends_on("icarusalg", type=("build", "run"))
    depends_on("icarus-data", type=("build", "run"))
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
    depends_on("fftw", type=("build", "run"))
    depends_on("fhicl-cpp", type=("build", "run"))
    depends_on("hep-concurrency", type=("build", "run"))
    depends_on("ifdh-art", type=("build", "run"))
    depends_on("ifdhc", type=("build", "run"))
    depends_on("ifbeam", type=("build", "run"))
    depends_on("tbb", type=("build", "run"))
    depends_on("geant4", type=("build", "run"))
    depends_on("icarus-signal-processing", type=("build", "run"))
    #depends_on("icarusutil", type=("build", "run"))
    depends_on("larsoft", type=("build", "run"))
    depends_on("larana", type=("build", "run"))
    depends_on("larcoreobj", type=("build", "run"))
    depends_on("larcore", type=("build", "run"))
    depends_on("lardataobj", type=("build", "run"))
    # larsimdnn might not be necessary, put here for consistency with sbnd
    depends_on("larsimdnn", type=("build", "run"))
    depends_on("lardata", type=("build", "run"))
    depends_on("larevt", type=("build", "run"))
    depends_on("pandora", type=("build", "run"))
    depends_on("larpandora", type=("build", "run"))
    depends_on("larpandoracontent", type=("build", "run"))
    depends_on("larreco", type=("build", "run"))
    depends_on("larvecutils", type=("build", "run"), when="@09.37.01.vec02p02")
    depends_on("larvecutils", type=("build", "run"), when="@09.37.01.vec03p02")
    depends_on("larsim", type=("build", "run"))
    depends_on("libwda", type=("build", "run"))
    depends_on("marley", type=("build", "run"))
    depends_on("nug4", type=("build", "run"))
    depends_on("nucondb", type=("build", "run"))
    depends_on("nutools", type=("build", "run"))
    depends_on("nurandom", type=("build", "run"))
    depends_on("nusimdata", type=("build", "run"))
    depends_on("postgresql", type=("build", "run"))
    depends_on("range-v3", type=("build", "run"))
    depends_on("sbndaq-artdaq-core", type=("build", "run"))
    depends_on("sbnobj", type=("build", "run"))
    depends_on("sbncode", type=("build", "run"))
    depends_on("sqlite", type=("build", "run"))
    depends_on("trace", type=("build", "run"))
    depends_on("protobuf", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-tensorflow", type=("build", "run"))

    depends_on("dk2nudata", type=("build", "run"))
    depends_on("cry", type=("build", "run"))
    depends_on("dk2nugenie", type=("build", "run"))
    depends_on("genie", type=("build", "run"))
    depends_on("log4cpp", type=("build", "run"))
    depends_on("rstartree", type=("build", "run"))
    depends_on("root@6.28.12", type=("build", "run"))

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
        args = [
            "-DWireCell_INCLUDE_DIR={0}".format(self.spec["wirecell"].prefix.include), 
            "-DWireCell_LIBRARIES={0}".format(self.spec["wirecell"].prefix.lib),
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-Dicaruscode_FW_DIR=fw",
            "-Dicaruscode_WP_DIR={0}".format(self.spec["wirecell"].prefix),
            "-DCMAKE_PREFIX_PATH={0}/lib/python{1}/site-packages/torch:".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2),
                #self.spec["icarusutil"].prefix
            ),
            "-DCPPGSL_INC={0}".format(self.spec["cppgsl"].prefix.include),
            "-DTRACE_INC={0}".format(self.spec["trace"].prefix.include),
            "-DLIBWDA_INC={0}".format(self.spec["libwda"].prefix.include),
            "-DVDT_INCLUDE_DIR={0}".format(self.spec["vdt"].prefix.include),
            "-DVDT_LIBRARY={0}".format(self.spec["vdt"].prefix.lib),
            "-DSPDLOG_FMT_EXTERNAL=ON",
            self.define(
                "CMAKE_PREFIX_PATH",
                join_path(
               self.spec["py-tensorflow"].prefix.lib,
               "python{0}/site-packages/tensorflow".format(
                   self.spec["python"].version.up_to(2)
               ),
             )
           ),
           self.define(
               "TensorFlow_LIBRARIES",
               join_path(
               self.spec["py-tensorflow"].prefix.lib,
               "python{0}/site-packages/tensorflow".format(
                   self.spec["python"].version.up_to(2)
               ),
             ),
           ),
        ]
        return args

    def setup_build_environment(self, spack_env):
        #spack_env.prepend_path("JSONCPP_LIB", os.path.join(self.spec['jsoncpp'].prefix.lib64))
        #spack_env.prepend_path("JSONCPP_INC", os.path.join(self.spec['jsoncpp'].prefix.include))

        spack_env.prepend_path("ROOT_INCLUDE_PATH", os.path.join(self.spec['larcoreobj'].prefix.include))
        spack_env.prepend_path("CPLUS_INCLUDE_PATH", os.path.join(self.spec['larcoreobj'].prefix.include))
        spack_env.prepend_path("CPLUS_INCLUDE_PATH", os.path.join(self.spec['libuuid'].prefix.include))
        spack_env.prepend_path("CPLUS_INCLUDE_PATH", os.path.join(self.spec['nusimdata'].prefix.include))
        spack_env.prepend_path("C_INCLUDE_PATH", os.path.join(self.spec['larcoreobj'].prefix.include))
        spack_env.prepend_path("LARCOREOBJ_INC", os.path.join(self.spec['larcoreobj'].prefix.include))
        spack_env.prepend_path("LARCOREOBJ_LIB", os.path.join(self.spec['larcoreobj'].prefix.lib))
        spack_env.prepend_path("LARDATAOBJ_INC", os.path.join(self.spec['lardataobj'].prefix.include))
        spack_env.prepend_path("LARDATAOBJ_LIB", os.path.join(self.spec['lardataobj'].prefix.lib))
        #spack_env.prepend_path("WIRECELL_PATH", os.path.join(self.spec['wirecell'].prefix))
        #spack_env.prepend_path("WIRECELL_LIB", os.path.join(self.spec['wirecell'].prefix.lib))
        #spack_env.prepend_path("LD_LIBRARY_PATH", os.path.join(self.spec['wirecell'].prefix.lib))
        #spack_env.prepend_path("LD_LIBRARY_PATH", os.path.join(self.spec['jsoncpp'].prefix.lib64))
        #spack_env.prepend_path("WIRECELL_INC", os.path.join(self.spec['wirecell'].prefix.include))
        #spack_env.prepend_path("LARWIRECELL_INC", os.path.join(self.spec['larwirecell'].prefix.include))
        #spack_env.prepend_path("LARWIRECELL_LIB", os.path.join(self.spec['larwirecell'].prefix.lib))

        spack_env.set("WIRECELL_PATH", os.path.join(self.spec['wirecell'].prefix.share.wirecell))
        spack_env.set("WIRECELL_LIB", os.path.join(self.spec['wirecell'].prefix.lib))
        spack_env.set("WIRECELL_INC", os.path.join(self.spec['wirecell'].prefix.include))
        spack_env.set("LARWIRECELL_INC", os.path.join(self.spec['larwirecell'].prefix.include))
        spack_env.set("LARWIRECELL_LIB", os.path.join(self.spec['larwirecell'].prefix.lib))
        spack_env.set("JSONCPP_LIB", os.path.join(self.spec['jsoncpp'].prefix.lib64))
        spack_env.set("JSONCPP_INC", os.path.join(self.spec['jsoncpp'].prefix.include))

        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("SPDLOG_INC", self.spec["spdlog"].prefix.include)
        spack_env.set("SPDLOG_LIB", self.spec["spdlog"].prefix.lib)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        #spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        #for d in self.spec.traverse(
        #    root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        #):
        #    spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # FW search path
        spack_env.append_path("FW_SEARCH_PATH", os.path.join(self.build_directory, "fw"))
        #spack_env.append_path("CMAKE_PREFIX_PATH", self.spec['icarusutil'].prefix)
        # Cleaup.
        spack_env.set(
                "Torch_DIR",
                "{0}/lib/python{1}/site-packages/torch/share/cmake/Torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ))

        #sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Binaries.
        run_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        #for d in self.spec.traverse(
        #    root=False,
        #    cover="nodes",
        #    order="post",
        #    deptype=("link"),
        #    direction="children",
        #):
        #    run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # FW search path
        run_env.append_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
        # fcls
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
        # Add to wire-cell path
        #run_env.prepend_path("JSONCPP_LIB", os.path.join(self.spec['jsoncpp'].prefix.lib))
        #run_env.prepend_path("JSONCPP_INC", os.path.join(self.spec['jsoncpp'].prefix.include))
        #run_env.prepend_path("WIRECELL_PATH", os.path.join(self.spec['wirecell'].prefix))
        #run_env.prepend_path("WIRECELL_LIB", os.path.join(self.spec['wirecell'].prefix.lib))
        #run_env.prepend_path("LD_LIBRARY_PATH", os.path.join(self.spec['wirecell'].prefix.lib))
        #run_env.prepend_path("LD_LIBRARY_PATH", os.path.join(self.spec['jsoncpp'].prefix.lib))
        #run_env.prepend_path("WIRECELL_INC", os.path.join(self.spec['wirecell'].prefix.include))
        #run_env.prepend_path("LARWIRECELL_INC", os.path.join(self.spec['larwirecell'].prefix.include))
        #run_env.prepend_path("LARWIRECELL_LIB", os.path.join(self.spec['larwirecell'].prefix.lib))
        ## Cleaup.
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
        # FW search path
        spack_env.append_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
        # Add to wire-cell path
        run_env.prepend_path("WIRECELL_PATH", os.path.join(self.spec['wirecell'].prefix))
        # Cleanup.
        sanitize_environments(spack_env)
