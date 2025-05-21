# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
import spack.util.web
from spack.package import *


class ArtdaqRuncontrolGui(CMakePackage):
    """SBN Run Control software"""

    homepage = "https://github.com/SBNSoftware"
    url = "https://github.com/SBNSoftware/artdaq-runcontrol-gui"
    git_base = "https://github.com/SBNSoftware/artdaq-runcontrol-gui.git"
    list_url = "https://api.github.com/repos/SBNSoftware/artdaq-runcontrol-gui/tags"

    version("1.03.04", sha256="57273320a95de6abacf4a853b53507710bb505a3e33dd09b74e3fd1b0e2e94ea")
    
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("artdaq-daqinterface")
    depends_on("qt")
    depends_on("xmlrpc-c")
    depends_on("cetbuildtools", type="build")
    
    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(
                        spack.util.web.read_from_url(
                            self.list_url, accept_content_type="application/json"
                        )[2]
                    )
                    if d["name"].startswith("v")
                ],
            )
        )
