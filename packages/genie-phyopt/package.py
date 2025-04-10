# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class GeniePhyopt(Package):
    """Phyopt files used by genie."""

    homepage = "https://www.example.com"
    url = "file://" + os.path.dirname(__file__) + "/../../config/junk.xml"
    version(
        "2.12.10", "2cae8b754a9f824ddd27964d11732941fd88f52f0880d7f685017caba7fea6b7", expand=False
    )

    variant(
        "phyopt_name",
        default="dkcharm",
        multi=False,
        values=("dkcharm", "dkcharmtau"),
        description="Name of genie phyopt to use.",
    )

    baseurl = "https://scisoft.fnal.gov/scisoft/packages/genie_phyopt/v2_12_10/genie_phyopt-2.12.10-noarch-"
    resource(
        name="dkcharm",
        when="phyopt_name=dkcharm",
        url=baseurl + "dkcharm.tar.bz2",
        sha256="5764cc6e7fc23f721177761526b75725b73970cd941064c23563d9ccaa3de0dc",
    )

    resource(
        name="dkcharmtau",
        when="phyopt_name=dkcharmtau",
        url=baseurl + "dkcharmtau.tar.bz2",
        sha256="ff0ecafd9a9455e8c20963c608c666f7229324c3f43e69fa58902584de08532a",
    )

    def install(self, spec, prefix):
        val = spec.variants["phyopt_name"].value
        install_tree(
            "{0}/genie_phyopt/v{1}/NULL/{2}".format(
                self.stage.source_path, self.version.underscored, val
            ),
            "{0}/{1}".format(prefix, val),
        )
