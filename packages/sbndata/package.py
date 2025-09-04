# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install sbndata
#
# You can edit this file again by typing:
#
#     spack edit sbndata
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
import glob

class Sbndata(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/SBNSoftware/sbndata/archive/refs/tags/v01_07.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.

    version("01_07", sha256="a85f0a9fcd33a7a82688f000594161efcd765c73c139c54c004a36ae52469662")
    version("01_06", sha256="32a4ecab5a5196f488499c38259ad5088bba6c672abcc25085df0e14c1407012")
    version("01_05", sha256="ff40bd35813ff802931a049e051d0dcb572df3e6e76b2105779e4daeb7f4d637")
    version("01_04", sha256="7671b48e6649cf4a0f4488cafcc26f34a5eaca3539956edd716b9924e4101f48")
    version("01_02", sha256="d25a1f96e34453052e461450add56eddb1f3c299014af133acf4c3315cb26bd4")
    version("01_01", sha256="76afeec6f7b3870596e7e1f6d80e9ac255cc7e2171b798e7b868d1e2344272d9")
    version("01_00", sha256="2ef4b2cca5b9cf6a478d9f8febe7c10c75479375b87469c05d1e176dc649ae95")

    def install(self, spec, prefix):
        print(self.stage.source_path)
        src = glob.glob(self.stage.source_path)[0]
        install_tree(src, prefix)

    def setup_run_environment(self, env):
        env.set("SBN_DATA_VERSION", "v%s" % self.version.underscored)
        env.prepend_path("FW_SEARCH_PATH", "%s/Calorimetry" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/beamData" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/triggerDatabase" % self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", "%s" % self.prefix)
        env.prepend_path("PKG_CONFIG_PATH", "%s" % self.prefix)

