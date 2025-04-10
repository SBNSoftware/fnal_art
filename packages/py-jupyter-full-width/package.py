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
#     spack install py-jupyter-full-width
#
# You can edit this file again by typing:
#
#     spack edit py-jupyter-full-width
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyJupyterFullWidth(PythonPackage):
    """Add a button to allow jupyter to use the full browser width"""

    homepage = "https://github.com/JoaoFelipe/JupyterFullWidth"
    pypi = "jupyter_full_width/jupyter_full_width-1.2.0.tar.gz"

    version("1.2.0", sha256="9227f315962ce49713f6a9a5f58ca1985ccc666f2f77dc9429fe600b4ad0afd2")

    depends_on("py-jupyter", type="run")

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
