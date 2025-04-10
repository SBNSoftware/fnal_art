# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRplotmaker(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    pypi = "rplotmaker/rplotmaker-1.0.6.tar.gz"

    version("1.0.6", sha256="3e7b25f18472646800cd94022cd3d02620c74f13253efc40b39790c7b9ca072e")

    depends_on("py-setuptools", type="build")
    depends_on("r", type=("build", "run"))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
