# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyinotify(PythonPackage):
    """Linux filesystem events monitoring"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://github.com/seb-m/pyinotify"
    pypi = "pyinotify/pyinotify-0.9.6.tar.gz"

    version("0.9.6", sha256="9c998a5d7606ca835065cdabc013ae6c66eb9ea76a00a1e3bc6e0cfe2b4f71f4")

    depends_on("py-setuptools", type="build")

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
