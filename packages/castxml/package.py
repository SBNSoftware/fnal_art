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
#     spack install castxml
#
# You can edit this file again by typing:
#
#     spack edit castxml
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Castxml(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/CastXML/CastXML"
    url = "https://github.com/CastXML/CastXML/archive/v0.2.0.tar.gz"

    version("0.5.1", sha256="a7b40b1530585672f9cf5d7a6b6dd29f20c06cd5edf34ef34c89a184a4d1a006")
    version("0.3.6", sha256="e51a26704864c89036a0a69d9f29c2a522a9fa09c1009e8b8169a26480bb2993")
    version("0.3.5", sha256="397044081363da0f3e50aff995f71b68aedd194d034caa50869224a4e6784c3b")
    version("0.3.4", sha256="a597ef37fe2b43fe3cf2c0c4e2ed0069d5aba2714016c319ac47787760859df4")
    version("0.3.3", sha256="9b8b9d6dd16dfa79c2291c025551b71654856cf525447e3616cae8f1c0a30e0f")
    version("0.3.2", sha256="d772f426241fbbfe687323656d9b232ea86fe557a627f0e8efa17587d1b97c9d")
    version("0.3.1", sha256="eccd8b086c05b3424e6582ff72c93b398fec3eb0e0855cdfef56cfcd952e47f5")
    version("0.3.0", sha256="904c242cb61cb31c447a5ccbb9005d2961c2a86beaf5739a623d0636949d1119")
    version("0.2.1", sha256="1f01149af1c58e59500e24cade8033e98a16001aa6a0f666643bbc9e303a82b0")
    version("0.2.0", sha256="626c395d0d3c777b5a1582cdfc4d33d142acfb12204ebe251535209126705ec1")

    # FIXME: Add dependencies if required.
    depends_on('llvm@15.0.7')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
