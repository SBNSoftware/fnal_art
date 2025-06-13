# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class GoJsonnet(Package):
    """
        The name Jsonnet is a portmanteau of JSON and sonnet, 
        pronounced "jay sonnet".  

        A macro expansion JSON source generating JSON, YAML, INI, 
        and other formats.

        This an implementation of Jsonnet in pure Go. 
        It is a feature complete, production-ready implementation. 
        It is compatible with the original Jsonnet C++ implementation. 
        Bindings to C and Python are available (but not battle-tested yet).
    """


    homepage = "https://github.com/google/go-jsonnet/"
    #url = "https://github.com/google/go-jsonnet/archive/refs/tags/v0.19.1.tar.gz"
    git = "https://github.com/google/go-jsonnet.git"

    maintainers = ["marcmengel", "chissg"]

    depends_on("go",type="build") 

    version("0.19.1", tag="v0.19.1")
    version("0.17.0", tag="v0.17.0")


    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    def setup_build_environment(self, spack_env):
        cxxstd_flag = "cxx{0}_flag".format(self.spec.variants["cxxstd"].value)
        spack_env.append_flags("CXXFLAGS", getattr(self.compiler, cxxstd_flag))
        spack_env.append_flags("CGO_CXXFLAGS", getattr(self.compiler, cxxstd_flag))
        #spack_env.append_flags("CGO_CXXFLAGS", "-I../cpp-jsonnet")
        spack_env.set("GOPATH", self.spec.prefix)
 
    def install(self, spec, prefix):
        go = which("go") 
        git = which("git") 
        chmod = which('chmod')

        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.include.gojsonnet)
        git('submodule','init')
        git('submodule','update')

        go('install', '-x', './cmd/jsonnet')
        go('install', '-x', './cmd/jsonnetfmt')

        if self.spec.satisfies("platform=darwin"):
            ldflags = '-extldflags=-Wl,--unresolved-symbols=ignore-in-shared-libs'
        else:
            ldflags = '-extldflags=-Wl,-undefined,error'

        # build C bindings and install by hand after patching generated .h

        with working_dir('c-bindings'):

            go( 'build', 
                 '-p', str(make_jobs), 
                 '-buildmode=c-shared', 
                 '-ldflags', ldflags, 
                 '-x', '-o', 'libjsonnet.so')

            # Adjust the generated libjsonnet.h file, which is missing one of 
            # the C API functions
            # -- This is icky, icky (see:
            #      https://github.com/google/go-jsonnet/issues/562
            # )
            filter_file(
                "extern void jsonnet_json_destroy(struct JsonnetVm* vmRef, struct JsonnetJsonValue* v);", 
                "extern void jsonnet_json_destroy(struct JsonnetVm* vmRef, struct JsonnetJsonValue* v);\n"
                "extern char* jsonnet_realloc(struct JsonnetVm* vm, char* str, size_t sz);",
                "libjsonnet.h"
            )
            filter_file(
                "#include (.)internal.h(.)",
                "#include \\1gojsonnet/internal.h\\2",
                "libjsonnet.h"
            )
            install("*.so", prefix.lib)
            install("*.h", prefix.include.gojsonnet)
            # go install makes things readonly so you can't delete them later...
            # so fix that..

        chmod('-R','ug+w',prefix)
