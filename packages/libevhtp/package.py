# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libevhtp(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/criticalstack/libevhtp"
    url = "https://github.com/criticalstack/libevhtp/archive/1.2.18.tar.gz"

    maintainers = ["marcmengel"]

    version("1.2.18", sha256="316ede0d672be3ae6fe489d4ac1c8c53a1db7d4fe05edaff3c7c853933e02795")
    version(
        "1.2.17-beta", sha256="fe10b418a4b0bd071a2e55e6ef9bc5946ed5199d5f4acce67b3af4cceb32edff"
    )
    version(
        "1.2.17-alpha", sha256="88b7623c96791a60a13b311a9b6b28e1734a367390f0b27fcd36174b2492e6f8"
    )
    version("1.2.16", sha256="4c3f510b15873e9fc29299de0c5d4d257d1d910710e104e33439a17c27fc414b")
    version("1.2.15", sha256="f78ee8a34492e266fc1b6b9d4003825659df672da1cf918120217a0ee0d14ed3")

    depends_on("cmake", type="build")
    depends_on("libevent")
    depends_on("openssl")
    depends_on("oniguruma")

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)
