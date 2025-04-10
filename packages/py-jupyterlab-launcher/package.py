# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-jupyterlab-launcher
#
# You can edit this file again by typing:
#
#     spack edit py-jupyterlab-launcher
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyJupyterlabLauncher(PythonPackage):
    """This package is used to launch an application built using JupyterLab"""

    homepage = "http://jupyter.org/"
    pypi = "jupyterlab_launcher/jupyterlab_launcher-0.13.1.tar.gz"

    version("0.13.1", sha256="f880eada0b8b1f524d5951dc6fcae0d13b169897fc8a247d75fb5beadd69c5f0")

    depends_on("py-setuptools", type="build")
    depends_on("py-jupyter", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
