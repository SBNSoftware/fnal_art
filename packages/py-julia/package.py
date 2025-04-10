# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJulia(PythonPackage):
    """Julia/Python bridge with IPython support"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://julialang.org/"
    pypi = "julia/julia-0.5.6.tar.gz"

    version("0.5.6", sha256="378d0377f75bb0e3bfc4cce19a56d3bf5a9a7be38e370e3a7cf3359bf4cd0378")

    depends_on("py-setuptools", type="build")
    depends_on("julia", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
