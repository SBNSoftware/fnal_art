# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_INSTALL_RPATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Wirecell(Package):
    """Wire Cell Toolkit provides simulation, signal processing and reconstruction for LArTPC
    Borrowed from
    https://github.com/WireCell/wire-cell-spack/blob/master/repo/packages/wirecell-toolkit/package.py
    """

    homepage = "https://wirecell.github.io"
    url = "https://github.com/WireCell/wire-cell-toolkit/archive/refs/tags/0.13.0.tar.gz"

    version("0.29.1", sha256="9fee2e37162a2ebed61db155319f857a504d3b2805e6c4db163c4935af80e1cd")
    version("0.27.1", sha256="a8410a9e0524570e811f5cca2ea9fc636e48c048a5e67c5cee567b935515e176")
    version("0.24.3", sha256="040d819a3a81b953a42c8b4bb898acf6978cee45beea0361a2f3cdb602a6028c")
    version("0.24.1", sha256="0467a4dff51abac3661aa99c5f3cc5de1ba1607a7f357631a2fbf7dcdf01c8a9")
    version("0.17.0", sha256="f2807adb83c8c6960ccefe8002bd015d646a96ad181d2092848d2461b3b81eea")
    version("0.16.0", sha256="af04affc1642c6ea534c479f0e1701e74b43674c2ebc025a117849ac0aba9cee")
    version("0.14.0", sha256="f7d792ef3c73744b395a6880018a4ba3349f2c5ba2f96399ad1a4d17be8f6092")
    version("0.13.1", sha256="d9ce092f9ebae91607213b62bf015ac6ac08c33ce97b6fbd67494d42c1f75bdb")
    version("0.13.0", sha256="eedc7db7ce75d2f7ef1b23461d1a2d780fd8409187eb851ced1e8ab4b7a10d8e")
    version("0.12.2", sha256="83387ebe6a517353daae69b05e86dd274f66ba80e6b120fb219b5c260c383e21")
    version("0.11.2", sha256="56b46cad781948e21c36660032de3ca54d5d5fd6b7aa47cdc3d3d4a67770f831")
    version("0.10.9", sha256="a5a7f2d45c78c18e098f3afc10e6df06b0e94e062870535c927c0fab51e43bd8")

    variant(
        "cxxstd",
        default="17",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("jsoncpp")
    depends_on("jsonnet")

    depends_on("fftw")
    depends_on("eigen")
    depends_on("spdlog")
    depends_on("hdf5")
    depends_on("h5cpp")

    # Do not currently make use of TBB.  When we get back to this,
    # probably best to build ROOT with TBB support as well.
    # depends_on("tbb")
    depends_on("root@6:")

    # match what is listed in wire-cell-build/wscript
    depends_on("boost +system+filesystem+graph+thread+program_options+iostreams+stacktrace")

    patch("setprecisionfix.patch", when="@0.14.0")
    patch("boost_spline.patch", when="@0.14.0")

    def patch(self):
        with when("@:0.24.3 %gcc@13:"):
            filter_file(
                "#include <typeinfo>",
                "#include <typeinfo>\n#include<cstdint>",
                "util/inc/WireCellUtil/Dtype.h",
            )

    def patch(self):
        with when("@:0.27.1 %gcc@12:"):
            filter_file(
                "#include <iomanip>",
                "#include <iomanip>\n#include<sstream>",
                "aux/src/Logger.cxx",
            )

    def install(self, spec, prefix):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))

        cfg = "wcb"
        cfg += " --prefix=%s" % prefix
        cfg += " --boost-mt"
        cfg += " --boost-libs=%s --boost-includes=%s" % (
            spec["boost"].prefix.lib,
            spec["boost"].prefix.include,
        )
        cfg += " --with-root=%s" % spec["root"].prefix
        cfg += " --with-eigen=%s" % spec["eigen"].prefix
        cfg += " --with-eigen-include=%s" % spec["eigen"].prefix.include.eigen3
        cfg += " --with-jsoncpp=%s" % spec["jsoncpp"].prefix
        cfg += " --with-jsonnet=%s" % spec["jsonnet"].prefix
        # cfg += " --with-tbb=%s" % spec["tbb"].prefix
        # cfg += " --with-tbb=false"  # for now
        cfg += " --with-fftw=%s" % spec["fftw"].prefix
        if cxxstdflag:
            cfg += " --build-debug=" + cxxstdflag

        cfg += " configure"
        python = which("python")
        python(*cfg.split())
        filter_file(r"-std=c\+\+11", cxxstdflag, "build/c4che/_cache.py")
        python("wcb", "-vv")
        python("wcb", "install")
        return

    def setup_build_environment(self, spack_env):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        spack_env.append_flags("CXXFLAGS", cxxstdflag)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
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
        # Cleanup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
            flags.append("-Wno-error=unused-function")
        return (flags, None, None)
