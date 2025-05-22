# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPlotlyScientificPlots(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://pypi.org/project/plotly-scientific-plots"
    pypi = "plotly-scientific-plots/plotly-scientific-plots-0.1.0.6.tar.gz"

    version("0.1.0.6", sha256="cc00d2ca8e90430ac513e1447dbef86d2dfe8a5367e5e10eaaabaca6b89d0b7c")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-plotly", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
