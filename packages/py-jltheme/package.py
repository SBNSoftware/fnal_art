# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJltheme(PythonPackage):
    """Change Matplotlib rcParams to match the current JupyterLab theme.

    Adjusts Matplotlib axis labels, edge, face, and tick colors based
    upon which JupyterLab theme is in use.
    """

    homepage = "https://github.com/CGCFAD/jltheme"
    pypi = "jltheme/jltheme-0.1.2.tar.gz"

    version("0.1.2", sha256="75361cbd59c835d7d71b8c9c23dd9ddf4644bf67d7e2a42afa260de7c39aa028")

    depends_on("py-jupyter", type=("run"))
