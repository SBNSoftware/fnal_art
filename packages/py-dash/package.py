# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDash(PythonPackage):
    """A Python framework for building reactive web-apps"""

    homepage = "https://plotly.com/dash"
    pypi = "dash/dash-2.0.0.tar.gz"

    version("2.0.0", sha256="29277c24e2f795b069cb102ce1ab0cd3ad5cf9d3b4fd16c03da9671a5eea28a4")

    depends_on("py-setuptools", type="build")
    depends_on("py-flask", type=("build", "run"))
    depends_on("py-flask-compress", type=("build", "run"))
    depends_on("py-plotly", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
