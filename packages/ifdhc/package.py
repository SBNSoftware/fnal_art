# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack import *


class Ifdhc(MakefilePackage):
    """Data handling client code for intensity frontier experiments"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdhc"
    git_base = "https://cdcvs.fnal.gov/projects/ifdhc/ifdhc.git"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/ifdhc.v2_5_2.tbz2"

    version("2.7.2", sha256="03f1211c89c49dc4669344fce5321d3c45fcf68bf46a84368010edd2dcdb2630")
    version("2.7.1", sha256="cb8726506546ff49f8134024171dfc389dbfff74e66a19ba1a49aea767f5f510")
    version("2.7", sha256="49c3e9fbc5a1ebb80d8fb870e45ec9faa6577c001a8a073521b071d51dd93bb8")
    version("2.6.20", sha256="54cffb88be5c085dd2f3246507cf850299b780e2ab16cd8abce4360e200b4044")
    version("2.6.19", sha256="5499391378d6769da0b94b0e8eaea358d6c7be40673e4c97c5580c4e94bdaa24")
    version("2.6.11", sha256="988eb6bd2124174e0956b4415edcc3671ac87896a64852e9e99d8628c4fa1334")
    version("2.6.10", sha256="44ee19429ec3c55be54582fb9411b68ebba9c90ae3ee8b770faa702f599a3f49")
    version("2.6.9", sha256="46dadbba0acdf19644496fd7c3eff2a046f745e9fe9fe68f42b7c499df293596")
    version("2.6.8", sha256="9a60403d06463f34c988d45a3049b1e09409c4a44ac08f45da920dc2eab26ff5")
    version("2.6.7", sha256="365949d19faf14200b4fa0f80dd881fbd4bbcf7f4699bab5e43358119d4109b8")
    version("2.6.6", sha256="fc04576e5ae82740f6a1797ebeeac6855338eb028a43b178f3f66183f4bb583e")
    version("2.5.16", sha256="5455f58042c7b84826fc72e77d21e9f0a5ec7efe5f40435571c52fb4c0e226fd")
    version("2.5.12", sha256="e8a8af62e5e9917e51c88b2cda889c2a195dfb7911e09c28aeaf10f54e8abf49")
    version("2.5.14", sha256="66ab9126bb3cb1f8d8dafb69568569d8856ab6770322efc7c5064252f27a8fda")
    version("2.3.9", sha256="1acdff224f32c3eb5780aed13cf0f23b431623a0ebc8a74210271b75b9f2f574")
    version("2.5.4", sha256="48bf6807cb8b3092677768f763c1f18940d852d685424a1ea386acf7f1606608")
    version("2.3.10", sha256="4da290f5fc3c9d4344792176e19e1d3278f87a634ebc1535bbd9a91aae2bbf9b")
    version("2.5.2", git=git_base, tag="v2_5_2", get_full_repo=True)
    version("develop", git=git_base, branch="develop", get_full_repo=True)

    depends_on("python")
    depends_on("swig", type="build", when="@:2.5.0")
    depends_on("zlib")
    depends_on("uuid")
    depends_on("ifdhc-config")

    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("version.patch", level=1, when="@:2.4.5")

    parallel = False

    def patch(self):
        for hfile in (os.path.join("ifdh", "ifdh.h"), os.path.join("numsg", "numsg.h")):
            filter_file(r'^(\s*#\s*include\s+["<])../util/', r"\1", hfile)
        filter_file(r"(CFLAGS=.*) -Werror", r"\1", "util/Makefile")

    def url_for_version(self, version):
        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"

        return url.format(self.name, version.underscored)

    @property
    def build_targets(self):
        print("in build_targets...")
        uuidflags = " -L %s -I %s " % (
            self.spec["uuid"].prefix.lib,
            self.spec["uuid"].prefix.include,
        )
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )

       
        with when("@2.6.9"):
            # sshbuildshims build_ifdhc.sh:311
            cxxstdflag = "%s -Wno-unused-but-set-variable" % cxxstdflag

        return ("SHELL=/bin/bash", 
                "PYMAJOR=%s" % self.spec["python"].version[0],
                "PYTHON=%s" % self.spec["python"].command.path,
                "PYTHON_LIB=%s" % self.spec["python"].libs.directories[0],
                "PYTHON_INCLUDE=%s" % self.spec["python"].headers.directories[0],
                "ARCH=-g -DNDEBUG %s %s" % (cxxstdflag, uuidflags), 
                "all"
               )

    @property
    def install_targets(self):
        return ("SHELL=/bin/bash", "DESTDIR={0}/".format(self.prefix), "install")

    @run_after("install")
    def install_cfg(self):
        cmd = "cp {0}/ifdh.cfg {1}/ifdh.cfg".format(self.stage.source_path, self.spec.prefix)
        tty.warn("installing ifdh.cfg: {0}".format(cmd))
        os.system(cmd)

    @run_after("install")
    def is_built(self):
        ''' replicate build-shims checks '''
        assert os.path.exists(self.prefix.bin.ifdh)
        assert os.path.exists(self.prefix.inc + "/ifdh.h")
        assert os.path.exists(self.prefix.lib + "/libifdh.so")
        assert os.path.exists(self.prefix.lib + "/python/ifdh.so")

    def setup_build_environment(self, spack_env):
        spack_env.set("PYTHON_INCLUDE", self.spec["python"].prefix.include)
        spack_env.set("PYTHON_LIB", self.spec["python"].prefix.lib)
        spack_env.set("IFDHC_DIR", self.spec.prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.spec.prefix.bin)
        run_env.prepend_path("PYTHONPATH", self.spec.prefix.lib.python)
        run_env.set("IFDHC_DIR", self.spec.prefix)
        # put ifdhc_config bin path ahead of us that we saved in os.environ...
        run_env.prepend_path("PATH", os.environ.get("IFDHC_CONFIG_BIN",""))

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("PATH", self.spec.prefix.bin)
        # Non-standard, therefore we have to do it ourselves.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.spec.prefix.inc)
        spack_env.set("IFDHC_DIR", self.spec.prefix)
        spack_env.set("IFDHC_INC", self.spec.prefix.inc)
