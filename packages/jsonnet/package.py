# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Jsonnet(Package):
    "A data templating language looking like JSON that produces JSON."

    homepage = "https://jsonnet.org"
    url = "https://github.com/google/jsonnet/archive/v0.9.3.tar.gz"


    version("0.18.0", sha256="85c240c4740f0c788c4d49f9c9c0942f5a2d1c2ae58b2c71068107bc80a3ced4")
    version("0.12.1", sha256="257c6de988f746cc90486d9d0fbd49826832b7a2f0dbdb60a515cc8a2596c950")
    version("0.12.0", sha256="9285f44f73a61fbfb61b3447a622e8aff0c61580c61c4a92f69d463ea7f1624a")
    version("0.11.2", sha256="c7c33f159a9391e90ab646b3b5fd671dab356d8563dc447ee824ecd77f4609f8")

    variant(
        "cxxstd",
        default="17",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    def patch(self):
        with when("@:0.19.1 %gcc@13:"):
            filter_file(
                r"#include \<cstring\>",
                "#include <cstdint>\n#include <cstring>",
                "include/libjsonnet++.h"
            )


    def install(self, spec, prefix):
        "Install Jsonnet"
        # This can use bazel but we fall back to the crude Makefile in order to
        # avoid the dependency on bazel which brings in JDK.
        make()
        make("libjsonnet.so")
        make("libjsonnet++.so")
        mkdirp(prefix.bin)
        install("jsonnet", prefix.bin)
        mkdirp(prefix.lib)
        install("libjsonnet.so", prefix.lib)
        install("libjsonnet++.so", prefix.lib)
        mkdirp(prefix.include)
        install("include/libjsonnet.h", prefix.include)
        install("include/libjsonnet++.h", prefix.include)
        libs = find(prefix.lib, "libjsonnet*")
        for lib in libs:
            symlink(lib, prefix.lib + "/%s.0" % os.path.basename(lib))


    def setup_build_environment(self, spack_env):
        for cflag in ("-O3", "-DNDEBUG", "-g", "-fno-omit-frame-pointer"):
            spack_env.append_flags("CFLAGS_LOCAL", cflag)
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        spack_env.append_flags("CXXFLAGS_LOCAL", cxxstdflag)
