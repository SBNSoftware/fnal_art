# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cetpkgsupport(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = "https://cdcvs.fnal.gov/projects/cetpkgsupport"

    version("develop", branch="develop", git=homepage, get_full_repo=True)
    version("v1_14_01", sha256="c834b6b439f05cee811989f1877c8862b4962bd8ddf61e7e4e80616396bdee34")
    version("1.14.01", sha256="c834b6b439f05cee811989f1877c8862b4962bd8ddf61e7e4e80616396bdee34")

    depends_on("cmake")

    def url_for_version(self, version):
        if str(version)[0] in "0123456789":
            url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"
            return url.format(self.name, version.underscored)
        else:
            url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.{1}.tbz2"
            return url.format(self.name, version)
