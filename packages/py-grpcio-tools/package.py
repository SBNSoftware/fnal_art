# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrpcioTools(PythonPackage):
    """HTTP/2-based RPC framework."""

    homepage = "https://grpc.io/"
    url = "https://pypi.io/packages/source/g/grpcio-tools/grpcio-tools-1.35.0.tar.gz"
    version("1.59.0", sha256="aa4018f2d8662ac4d9830445d3d253a11b3e096e8afe20865547137aa1160e93")
    version("1.58.0", sha256="6f4d80ceb591e31ca4dceec747dbe56132e1392a0a9bb1c8fe001d1b5cac898a")
    version("1.35.0", sha256="9e2a41cba9c5a20ae299d0fdd377fe231434fa04cbfbfb3807293c6ec10b03cf")

    depends_on("python@3.5:", when="@1.30:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-grpcio", type=("build", "run"))

    def setup_build_environment(self, env):
        pass

    def patch(self):
        pass
