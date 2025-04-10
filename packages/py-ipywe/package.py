# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIpywe(PythonPackage):
    """ipywidgets extensions for neutron scattering data analysis"""

    homepage = "https://github.com/neutrons/ipywe"
    pypi = "ipywe/ipywe-0.1.3a1.tar.gz"

    version("0.1.3a1", sha256="3fa853fc6ed12ac4bfcf7724641f7b32d4b1bc0815a27cf698559d83b45298ed")

    depends_on("py-setuptools", type="build")
    depends_on("py-ipywidgets", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
