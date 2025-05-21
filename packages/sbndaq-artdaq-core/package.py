# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
import spack.util.web
from spack.package import *


class SbndaqArtdaqCore(CMakePackage):
    """The toolkit currently provides SBNDAQ extensions to the artdaq-core
    functionality for data transfer, event building, event reconstruction."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/sbndaq/wiki"
    url = "https://github.com/SBNSoftware/sbndaq-artdaq-core/archive/v1_00_00of0.tar.gz"
    git_base = "https://github.com/SBNSoftware/sbndaq-artdaq-core.git"
    list_url = "https://api.github.com/repos/SBNSoftware/sbndaq-artdaq-core/tags"

    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("1.08.00of0", sha256="4b839b28a9ac17b89a3c33f840fb7cd3ae96f13c12ab461794a7dd04b144b024")
    version("1.08.00", sha256="02c5008d8b411f3edd8a67be9ae4f51fba840533693c624981a649679c0e43dd")
    version("1.07.01", sha256="edf3b55215c7b9f034188eeebad33654d938f60073cc568e4ba8f5f23c0515a7")
    version("1.07.00of0", sha256="e57e4ffe9a0824af9a0d3ce5f692bb9c7a0d1fbc40256991b2f47c888919be72")
    version("v1_00_00of0", git=git_base, tag="v1_00_00of0", get_full_repo=True)
    version("v1_00_00of2", git=git_base, tag="v1_00_00of2", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    
    variant("icarus", default=False, description="Build ICARUS-specific parts of the package")
    variant("sbnd", default=False, description="Build SBND-specific parts of the package")

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(
                        spack.util.web.read_from_url(
                            self.list_url, accept_content_type="application/json"
                        )[2]
                    )
                    if d["name"].startswith("v")
                ],
            )
        )

    #patch("cetmodules2.patch", when="@develop")
    patch("v1_00_00of0.patch", when="@v1_00_00of0")
    patch("v1_00_00of2.patch", when="@v1_00_00of2")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("messagefacility")
    depends_on("cetmodules", type="build")
    depends_on("artdaq-core")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("boost")
    depends_on("trace")

    def setup_run_environment(self, spack_env):
        spack_env.set("MRB_QUALS", "both")

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DICARUS_BUILD={0}".format("TRUE" if "+icarus" in self.spec else "FALSE"),
            "-DSBND_BUILD={0}".format("TRUE" if "+sbnd" in self.spec else "FALSE"),
        ]
        return args
