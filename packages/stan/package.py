# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stan(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mc-stan.org/"
    url = "https://github.com/stan-dev/stan/archive/v2.26.0.tar.gz"

    maintainers = ["marc.mengel@gmail.com"]

    version(
        "2.26.0-rc1", sha256="a0328ba63267c7417185af390613b8ce4e833766e5c7441f615eaa8ec7da3cbe"
    )
    version("2.26.0", sha256="3b6ff0cbeddaa5b0f94692862d7a2266d12c3e7a6833ea0f5c7c20ff7b28907a")
    version(
        "2.25.0-rc1", sha256="9b34c1d1ff11c7e9d8b67ec6d8b685e7a92b6711dd63c04e65e3d35780d22bed"
    )
    version("2.25.0", sha256="9c2f936be00f28f95b58e061e95b5a81990b978001eb9df5b03f7803906b1d78")
    version("2.24.0", sha256="f398098eb030036d23b2a8e131598bc89c2e4fa5e85be9ab1d0a8b0d91739f99")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path + "/src/stan", prefix.include)

    def setup_run_environment(self, run_env):
        # run_env.prepend_path('PYTHONPATH', self.prefix.bin)
        # run_env.prepend_path('PYTHONPATH', self.prefix + '/python')
        pass
