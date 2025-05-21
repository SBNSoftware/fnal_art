# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
import spack.util.web
from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class SbndaqArtdaq(CMakePackage):
    """Readout software for the SBN experiments"""

    homepage = "https://github.com/SBNSoftware"
    url = "https://github.com/SBNSoftware/sbndaq-artdaq"
    git_base = "https://github.com/SBNSoftware/sbndaq-artdaq.git"
    list_url = "https://api.github.com/repos/SBNSoftware/sbndaq-artdaq/tags"


    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("1.08.01", sha256="8c636599ef5d4e02771a82e3e19c65676665df5f789b8bee60a83d4b42779d29")
    version("1.08.00", sha256="156554958cc4894b1fc0c506f512bd4ae3ff69a2ca694ba5c03a1795587ef66a")
    version("1.07.02", sha256="899ff79d5369a6d54462016537e366c9f4439723b6836ad91464b954c646135b")
    version("1.07.01", sha256="d4eb0f9cf5187c0059eef80234d27e96ca29938317c049833caddb624903ed62")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    
    variant("icarus", default=False, description="Build ICARUS-specific parts of the package")
    variant("sbnd", default=False, description="Build SBND-specific parts of the package")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("artdaq")
    depends_on("sbndaq-artdaq-core")
    depends_on("sbndaq-artdaq-core+icarus", when="+icarus")
    depends_on("sbndaq-artdaq-core+sbnd", when="+sbnd")
    depends_on("caenvmelib")
    depends_on("caencomm")
    depends_on("caendigitizer")
    depends_on("libpqxx")
    depends_on("artdaq-epics-plugin") # For FindEPICS.cmake
    depends_on("epics-base")
    depends_on("cppzmq")
    depends_on("jsoncpp")
    depends_on("wibtools", when="+sbnd")
    #depends_on("windriver", when="+sbnd")
    depends_on("redis")
    depends_on("cetmodules", type="build")

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
    
    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DICARUS_BUILD={0}".format("TRUE" if "+icarus" in self.spec else "FALSE"),
            "-DSBND_BUILD={0}".format("TRUE" if "+sbnd" in self.spec else "FALSE"),
            "-DSPACK_BUILD=1"
        ]
        return args

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
