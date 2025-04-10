# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

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


class Bxdecay0(CMakePackage):
    """SignalProcessing for icarus
    framework for particle physics experiments.
    """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/bxdecay0"
    git = "https://github.com/BxCppDev/bxdecay0.git"
    url = "https://github.com/BxCppDev/bxdecay0/archive/bxdecay0.1.0.5.tar.gz"
    list_url = "https://api.github.com/repos/BxCppDev/bxdecay0/tags"

    version("1.1.0", sha256="f10fc4ae1783ff0118f2f75ad9156222a5b05f6825eb1419132f4231392cbf70")
    version("1.0.9", sha256="82c2373f10b41709030b8769a39ad8174beeaa04da524aaf2deba2493eef582d")
    version("1.0.7", sha256="f11f3f7e0bdcbdd73efe1e0eb28b5c004c18aee3c6ce359af9c0d8b4cab58469")

    version("develop", branch="develop", get_full_repo=True)

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

    patch("bxdecay0.patch", when="@1.0.7")

    def patch(self):
        with(when("@:1.1.1 %gcc@13:" )):
            filter_file(
                '#include <string>',
                '#include <cstdint>\n#include <string>',
                'bxdecay0/particle.h',
            )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # Build-only dependencies.
    depends_on("cmake@3.11:")
    depends_on("pkgconfig", type="build")

    # Build and link dependencies.
    depends_on("gsl", type=("build", "run"))

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def url_for_version(self, version):
        url = "https://github.com/BxCppDev/{0}/archive/refs/tags/{1}.tar.gz"
        return url.format(self.name, version)

    def cmake_args(self):
        # Set CMake args.
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
          "-DGSL_ROOT_DIR={0}".format(self.spec["gsl"].prefix),
        ]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env)
