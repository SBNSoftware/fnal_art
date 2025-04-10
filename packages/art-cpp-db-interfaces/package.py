# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ArtCppDbInterfaces(Package):
    """Header only library of C++ interfaces to
    Scientific Computing Division storage services."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/art_cpp_db_interfaces"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/art_cpp_db_interfaces.v1_4.tbz2"

    maintainers = ["marcmengel"]

    version("1_4", sha256="a4500c065d4bf595f23b5ce2e1748cf590cc1b7468189774aa4b7b5d79f16d78")

    depends_on("postgresql", "run")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
