# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install py-pygccxml
#
# You can edit this file again by typing:
#
#     spack edit py-pygccxml
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyPygccxml(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://pygccxml.readthedocs.io/en/develop/"
    url = "https://github.com/CastXML/pygccxml/archive/v2.0.1.tar.gz"

    version("2.2.1", sha256="9815a12e3bf6b83b2e9d8c88335fb3fa0e2b4067d7fbaaed09c3bf26c6206cc7")
    version("2.0.1", sha256="25c6f693da741139c538d751b4bee1408764a4470c4f5ee982ac2611032cebc2")
    version("2.0.0", sha256="b941698700bc52c4aa9014d8d7d687c35b82273e1b5857c81bf1ea2b384ec90e")
    version("1.9.1", sha256="2fb4e18f7a3ae039a05230ca58f11e1fc925c8643f926a1be481bb4338414a95")

    depends_on("python", type=("build", "run"))
    depends_on("castxml", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    def build_args(self, spec, prefix):
        args = []
        return args
