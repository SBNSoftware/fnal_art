# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nucondb(MakefilePackage):
    """Data handling client code for intensity frontier experiments"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nucondb"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/nucondb.v2_2_10.tbz2"
    git = "https://cdcvs.fnal.gov/projects/ifdhc-nucondb"

    version("2.6.1", sha256="fbf59259e8cd75334b4ad17d3da46519d35c5c81ccf55b8df2d19f664fe016b9")
    version("2.5.23", sha256="30399133b64548affd3522eb16346a1fc85f36ba4300fce51730a208a8022f24")
    version("2.5.22", sha256="bd468d5b64909e3951342eacef30440e1eaca5d32add991fe6cc36b46f1c5f65")
    version("2.5.17", sha256="5b9bd0e8e6359edb594416847a946214376f013afedebbd861ebd6556d45823f")
    version("2.5.16", sha256="2de3a199407a378ea62f76652bc0945065d6636c7f7a02e5fafa9667f4ae833a")
    version("2.5.2", tag="v2_5_2", get_full_repo=True)
    version("2.4.8", tag="v2_4_8", get_full_repo=True)
    version("2.3.0", tag="v2_3_0", get_full_repo=True)
    version("2.2.10", tag="v2_2_10", get_full_repo=True)

    parallel = False

    build_directory = "src"

    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("ifdhc")
    depends_on("ifbeam")
    depends_on("libwda")

    def patch(self):
        filter_file(
            r"catch \(WebAPIException we\)", "catch (WebAPIException &we)", "src/nucondb.cc"
        )

    def url_for_version(self, version):
        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"
        return url.format("ifdhc-" + self.name, version.underscored)

    @property
    def build_targets(self):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        return [
            "LIBWDA_FQ_DIR=" + self.spec["libwda"].prefix,
            "LIBWDA_LIB=" + self.spec["libwda"].prefix.lib,
            "IFDHC_FQ_DIR=" + self.spec["ifdhc"].prefix,
            "IFBEAM_FQ_DIR=" + self.spec["ifbeam"].prefix,
            "IFDHC_LIB=" + self.spec["ifdhc"].prefix.lib,
            "ARCH=" + cxxstdflag,
        ]

    @property
    def install_targets(self):
        return ("DESTDIR={0}/".format(self.prefix), "install")

    def setup_build_environment(self, spack_env):
        spack_env.set("NUCONDB_DIR", self.prefix)

    def setup_run_environment(self, run_env):
        run_env.set("NUCONDB_DIR", self.prefix)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("NUCONDB_DIR", self.prefix)
