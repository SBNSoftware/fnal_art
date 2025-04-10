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
#     spack install stan-math
#
# You can edit this file again by typing:
#
#     spack edit stan-math
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class StanMath(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/stan-dev/math/archive/v4.0.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version("4.0.0", sha256="99ccd238eb2421be55d290a858ab5aa31022eded5c66201fcee35b2638f0bb42")
    version("3.5.0-rc1", sha256="f867613f8b908a02aac1df196d028bd1aad2c19bb40f2b454940ef7dfaeecfdc")
    version("3.4.0-rc1", sha256="59703645dc5b1fe7e3dab71737a282ed4dd4938f80100c8736e072d6c2ecb001")
    version("3.4.0", sha256="3e768d1c2692543d3560f9d954d19e58fd14c9aaca22f5140c9f7f1437ddccf9")
    version("3.3.0", sha256="fb96629fd3e5e06f0ad4c03a774e54b045cc1dcfde5ff65b6f78f0f05772770a")

    def install(self, spec, prefix):
        # NOTE: there are some tests that require building, but these are mostly
        #       targeted at Stan developers.
        #       We're just going to unwind the tarball and install the headers,
        #       which are all users need

        # lib contains a bunch of library dependencies that we're
        # obtaining via Spack instead
        os.system("rm -rf lib")
        install_tree(self.stage.source_path, prefix)

    def setup_build_environment(self, spack_env):
        pass
