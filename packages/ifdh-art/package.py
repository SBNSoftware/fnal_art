# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
import spack.util.web
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
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class IfdhArt(CMakePackage):
    """The ifdh_art package provides ART service access to the libraries
    from the ifdhc package."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdh-art/wiki"
    git = "https://github.com/art-framework-suite/ifdh-art.git"
    url = "https://github.com/art-framework-suite/ifdh-art/archive/refs/tags/v2_12_05.tar.gz"
    list_url = "https://api.github.com/repos/art-framework-suite/ifdh-art/tags"

    version("2.18.00", sha256="890665a7de3bab4b2d34efe21038dca66d3c99e24f064c476c9b5b028eff959b")
    version("2.17.06", sha256="fed29b9ca80e8e956b8d60e915f94972ee50ed42fce346dd6f2151420d22b455") 
    version("2.17.04", sha256="f65650ce3728620968eee6c7612469c1a669e34e84e4251dda0c9d7c9a00ac31")
    version("2.17.01", sha256="40874945c3af876bef9b668e296726ab834bc9bcd6cd11c6ff73fcfc29dd870b")
    version("2.17.00", sha256="d6f10c2516450550f48441f58867456a3dbdccd1c80d6a61bff7095becba3751")
    version("2.16.02", sha256="a39d83228f4c41463ef95bb44abf4f8c857c1c27d91d4e0376f623a99a82ba11")
    version("2.15.06", sha256="a3bf2771c1a3a1cd537128eb1a3a7a4848ea0b97471db8b6d250db192d668a7d")
    version("2.13.14", sha256="e71b3413ac8bad210d6e960ee3c17de92bd34958510c020f1c2005efc5269989")
    version("2.13.13", sha256="215d738a0cb4a40c51346c4eaf36358667a1ca52aa703bc89e427fc493603d82")
    version("2.13.00", sha256="d9b59c4181051d6b86ee346c562faaac7d4c5c0eeef37f159e2b1757859d4516")
    version("2.12.05", sha256="f783e6e06d6d26f58b44c68d76d6b404bfe80a57918f4d7490090495f3ef35d1")
    version("2.12.04", sha256="10999a6cbf1f55f51dcba91c9631a2dc06d04ffc6230bfe3b3421f84ccb207b1")
    version("develop", branch="develop", get_full_repo=True)
    version("MVP1a", branch="feature/Spack-MVP1a")

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/{0}/archive/v{1}.tar.gz"
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

    patch("cetmodules2.patch", when="@develop")
    patch("v2_12_05.patch", when="@2.12.05")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("art")
    depends_on("ifdhc")
    depends_on("ifbeam")
    depends_on("nucondb")
    depends_on("libwda")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)

    @run_after("install")
    def rename_README(self):
        import os

        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename(
                join_path(self.spec.prefix, "README"),
                join_path(self.spec.prefix, "README_%s" % self.spec.name),
            )
