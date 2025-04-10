# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gm2(Package):
    """Wrapper for packages for gm2 experiment"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/gm2"
    url = "https://cdcvs.fnal.gov/redmine/projects/gm2"

    maintainers = ["marcmengel"]

    version("9.70.00")

    depends_on("git", type=("build", "run"))
    depends_on("gitflow", type=("build", "run"))
    depends_on("ninja", type=("build", "run"))
    depends_on("cetpkgsupport", type=("build", "run"))
    depends_on("gm2pip", type=("build", "run"))
    depends_on("art", type=("build", "run"))
    depends_on("gm2tracker", type=("build", "run"))
    depends_on("gm2calo", type=("build", "run"))
    depends_on("gm2templates", type=("build", "run"))
    depends_on("gm2ringsim", type=("build", "run"))
    depends_on("gm2analyses", type=("build", "run"))
    depends_on("gm2reconeast", type=("build", "run"))
    depends_on("gm2field", type=("build", "run"))
    depends_on("gm2db", type=("build", "run"))
    depends_on("gallery", type=("build", "run"))

    def install(self, spec, prefix):
        # packages have to install *something*, so a README...
        f = open(prefix + "README.gm2pip", "w")
        f.write("gm2pip -- wrapper product for gm2 python dependencies\n")
        f.close()
