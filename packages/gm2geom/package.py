# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gm2geom(CMakePackage):
    """Gm2 experiment tracking code"""

    homepage = "https://redmine.fnal.gov/projects/gm2geom"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2geom.v9_60_00.tbz2"
    git_base = "https://cdcvs.fnal.gov/projects/gm2geom"

    version("10.16.00", sha256="a98d877a5b11d93454dfc7251a4280ab268aa8edf58d249253cbe64bd1ce24c6")
    version("spack_branch", branch="feature/mengel_spack", git=git_base, get_full_repo=True)

    def url_for_version(self, version):
        return (
            "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2geom.v%s.tbz2"
            % version.underscored
        )


    depends_on("pkgconfig", type="build")
    depends_on("cetpkgsupport", type=("build"))
    depends_on("cetbuildtools", type=("build"))
    depends_on("artg4", type=("build", "run"))
    depends_on("xerces-c", type=("build", "run"))
    depends_on("art", type=("build", "run"))
    depends_on("canvas", type=("build", "run"))
    depends_on("cetmodules", type=("build"))

    variant("cxxstd", default="17")

    def cmake_args(self):
        args = [
            "-DCXX_STANDARD=%s" % self.spec.variants["cxxstd"].value,
            "-DOLD_STYLE_CONFIG_VARS=True", 
            "-DCMAKE_MODULE_PATH={0}".format(
                          self.spec['cetmodules'].prefix.Modules.compat),
            "-DUPS_PRODUCT_VERSION=v{0}".format(self.spec.version.underscored),
        ]
        return args

    def setup_build_environment(self, env):
        env.set("CETBUILDTOOLS_VERSION", self.spec['cetbuildtools'].version)
        env.set("CANVAS_DIR", self.spec['canvas'].prefix)

