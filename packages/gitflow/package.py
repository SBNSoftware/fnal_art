# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gitflow(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/nvie/gitflow"
    url = "https://github.com/nvie/gitflow/archive/refs/tags/0.4.1.tar.gz"

    maintainers = ["marcmengel"]

    version("0.4.1", sha256="c1271b0ba2c6655e4ad4d79562f6a910c3b884f3d4e16985e227e67f8d95c180")
    version("0.4", sha256="c6b54e2acb7bb0819c33179e6929a9dc6236af1384257337b720ac35e21e7b17")
    version("0.3", sha256="75f27963276c9dd8c56d04225c5f2757afc6f38987eeb73161ba65e57a9afab7")

    # depends_on('bash','run')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix)
