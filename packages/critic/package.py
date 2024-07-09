# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.environment import NameValueModifier
from spack.util.prefix import Prefix


class PrependEnv(NameValueModifier):
    def execute(self, env):
        tty.debug("PrependEnv: {0}+{1}".format(self.name, str(self.value)), level=3)
        prepend_env_value = env.get(self.value, None)
        if prepend_env_value:
            environment_value = env.get(self.name, None)
            directories = (
                prepend_env_value.split(self.separator) + environment_value.split(self.separator)
                if environment_value
                else []
            )
            env[self.name] = self.separator.join(directories)


class Critic(CMakePackage, FnalGithubPackage):
    """Compatibility tests for the art and gallery applications of the art
    suite.
    """

    homepage = "https://art.fnal.gov/"
    repo = "art-framework-suite/critic"

    version_patterns = ["v2_12_02"]

    version("develop", branch="develop", get_full_repo=True)
    version("2.14.00", sha256="cefb90d3ab4de47a3a06fddf8f8c5fd4bf7fde62ab24b24a5bb1b97758c2e972")
    version("2.13.06", sha256="92359d75c947047a5a8753de3cbdcfa36dcf320420ed46ac3c0c39ea41cfb4a4")
    version("2.13.05", sha256="7f2470ef8360423e0b1f509538a1ae2df0e42cd231ea48fd2fc225b7181f96f2")
    version("2.13.03", sha256="96f62ff84e09fab7359f4d890e1bb9939cdea35b702a733663187483536da74e")
    version("2.13.01", sha256="bc5aac156904a34161db5af23a0e0952c648614a91961ae631dace815a903ec4")
    version("2.12.04", sha256="0ec37fe12f9433ea9df4ec0bd33e667b3dd10a45137b2abc4292f6b08460b225")
    version("2.12.03", sha256="13ae221a5060eb37de3c57c3b74e707c3bb2bd6352995fc640bfbb6e841bcfca")
    version("2.12.02", sha256="9dc9e20c97ecd7e967851546dc12dde9a9768b95c14b8f5c64b0ef11a158730d")

    cxxstd_variant("17", "20", "23", default="17", sticky=True)
    conflicts("cxxstd=17", when="@2.14.00:")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetmodules", type="build")
    depends_on("clhep@2.4.1.0:")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("gallery")
    depends_on("hep-concurrency")
    depends_on("messagefacility")
    depends_on("root+python")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        # Binaries.
        env.prepend_path("PATH", prefix.bin)
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # ... and in the interpreter.
        env.env_modifications.append(PrependEnv("LD_LIBRARY_PATH", "CET_PLUGIN_PATH"))
        # Cleanup.
        sanitize_environment(env, "PATH", "CET_PLUGIN_PATH", "LD_LIBRARY_PATH")
