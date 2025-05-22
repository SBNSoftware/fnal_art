# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlabTemplates(PythonPackage):
    """Support for jupyter notebook templates in jupyterlab"""

    homepage = "https://github.com/jpmorganchase/jupyterlab_templates"
    pypi = "jupyterlab_templates/jupyterlab_templates-0.3.1.tar.gz"

    version("0.3.1", sha256="7ee348ea0318033fcbd9274658c418d6cadafe89e9b3197e89c97f1cfde3eaff")

    depends_on("py-jupyter-packaging", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-jupyter", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
