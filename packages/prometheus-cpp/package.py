# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install prometheus-cpp
#
# You can edit this file again by typing:
#
#     spack edit prometheus-cpp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PrometheusCpp(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/jupp0r/prometheus-cpp/"
    url = "https://github.com/jupp0r/prometheus-cpp/archive/refs/tags/v0.12.2.zip"

    # notify when the package is updated.
    # maintainers = ['marcmengel',]

    version("0.12.2", sha256="7cbf90b89a293b4db3ff92517deface71a2edd74df7146317f79ae2a6f8c4249")
    version("0.12.1", sha256="3f9e623381a81d99e3a61053b0e671e9b5db209588a9364a980c237a19149150")
    version("0.12.0", sha256="a605904a2d40bc823bb121b2d25eb26b61065e29f0baaee6590b8058808a2cef")
    version("0.11.0", sha256="396a31ec459e0c676c75a4cc94ab33c0728949b4d32b1d3418262cc6acc16d1b")

    depends_on("pkgconfig")

    def cmake_args(self):
        args = [
            "-DENABLE_PULL=OFF",
            "-DENABLE_COMPRESSION=ON",
            "-DENABLE_TESTING=OFF",
            "-DUSE_THIRDPARTY_LIBRARIES=OFF",
            "-DTHIRDPARTY_CIVETWEB_WITH_SSL=OFF",
            "-DOVERRIDE_CXX_STANDARD_FLAG=ON",
            "-DGENERATE_PKGCONFIG=ON",
        ]
        return args
