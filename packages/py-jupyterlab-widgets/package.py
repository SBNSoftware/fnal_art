# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlabWidgets(PythonPackage):
    """A JupyterLab 3.0 extension for Jupyter/IPython widgets."""

    homepage = "https://github.com/jupyter-widgets/ipywidgets"
    pypi = "jupyterlab_widgets/jupyterlab_widgets-1.0.2.tar.gz"

    version("1.0.2", sha256="7885092b2b96bf189c3a705cc3c412a4472ec5e8382d0b47219a66cccae73cfa")

    depends_on("py-jupyter-packaging", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-jupyter", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
