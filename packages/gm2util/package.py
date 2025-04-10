# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gm2util(CMakePackage):
    """gm2 experiment utility code"""

    homepage = "https://www.example.com"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2util.v1_2_3.tbz2"

    maintainers = ["marcmengel", "gartung"]

    def url_for_version(self, version):

        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"
        # url = 'https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    depends_on("cetpkgsupport", type=("build", "run"))
    depends_on("artg4", type=("build", "run"))
    depends_on("libpqxx", type=("build", "run"))
    depends_on("eigen", type=("build", "run"))
    depends_on("cetmodules", type=("build"))

    variant("cxxstd", default="17")

    def setup_run_environment(self, env):
        self.tf_setup(env)
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)

    def setup_dependent_build_environment(self, env, dep):
        self.tf_setup(env)
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)


    def cmake_args(self):
        args = [
            "-DCXX_STANDARD=%s" % self.spec.variants["cxxstd"].value,
            "-DOLD_STYLE_CONFIG_VARS=True", 
            "-DCMAKE_MODULE_PATH={0}".format(
                          self.spec['cetmodules'].prefix.Modules.compat),
            "-DUPS_PRODUCT_VERSION=v{0}".format(self.spec.version.underscored),
        ]
        return args
