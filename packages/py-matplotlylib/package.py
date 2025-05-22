# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMatplotlylib(PythonPackage):
    """Package to render matplotlib figures in plotly."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://pypi.org/project/matplotlylib"
    pypi = "matplotlylib/matplotlylib-0.1.0.tar.gz"

    version("0.1.0", sha256="c7f5fa7f842742d9385b6961f88b9a992a749391a5f7229cc8be325f712c1fce")

    depends_on("py-setuptools", type="build")
    depends_on("py-plotly", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
