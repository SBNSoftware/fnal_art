# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack.package import *


class Rstartree(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage =  "https://github.com/virtuald/r-star-tree"
    url = "https://github.com/virtuald/r-star-tree.git"
    git = "https://github.com/virtuald/r-star-tree.git"

    maintainers = ["marcmengel"]

    version("0.2", git=git, commit="65f37ac95a77315fde1d24ab8081ab82540c1d50")
    version("0.1", git=git, commit="845ae41c122b4302e5a7cc53614c33f4c077db0a")

    def install(self, spec, prefix):
        makedirs(prefix.include.RStarTree)
        install("RStarBoundingBox.h", prefix.include.RStarTree) 
        install("RStarTree.h", prefix.include.RStarTree) 
        install("RStarVisitor.h", prefix.include.RStarTree) 
