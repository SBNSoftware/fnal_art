# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Log4cpp(AutotoolsPackage):
    """A library of C++ classes for flexible logging to files (rolling),
    syslog, IDSA and other destinations. It is modeled after the Log for Java
     library (https://www.log4j.org), staying as close to their API as is
    reasonable."""

    homepage = "https://sourceforge.net/projects/log4cpp/"
    url = "https://newcontinuum.dl.sourceforge.net/project/log4cpp/log4cpp-1.1.x%20%28new%29/log4cpp-1.1/log4cpp-1.1.3.tar.gz"

    version("1.1.3", "74f0fea7931dc1bc4e5cd34a6318cd2a51322041")

    def patch(self):
        patch("patch/log4cpp.patch")

    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    def setup_build_environment(self, spack_env):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        spack_env.append_flags("CXXFLAGS", cxxstdflag)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("PATH", self.spec.prefix.bin)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.spec.prefix.bin)
