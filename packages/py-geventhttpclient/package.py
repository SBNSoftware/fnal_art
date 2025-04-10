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
#     spack install srproxy
#
# You can edit this file again by typing:
#
#     spack edit srproxy
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyGeventhttpclient(PythonPackage):
    "A high performance, concurrent HTTP client library for python using gevent."

    homepage = "https://github.com/gwik/geventhttpclient"
    pypi = "geventhttpclient/geventhttpclient-1.4.4.tar.gz"

    version("1.4.4", sha256="f59e5153f22e4a0be27b48aece8e45e19c1da294f8c49442b1c9e4d152c5c4c3")

    depends_on("py-setuptools", type="build")
