# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySrproxy(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/cafana/SRProxy/"
    url = "https://github.com/cafana/SRProxy/archive/v00.44.tar.gz"

#    version("00.45", sha256="be614ac5637796f0a16f3480caacfd647abcfa8992a47556f63a5aefe4f2f85e")
    version("00.44", sha256="8bdefc5031033c847f2300aebd853b4ee71811fd63d4d360e85e58d41f956381")
    version("00.43", sha256="c64d6b567e3f49e52528bbd741fd849fd37a350cf1d8d59720c21af3646beade")
    version("00.35", sha256="dc78f8fe8b188728c361d8d02ce5aada9ddaf0b89713bd56feb83a1135cf2b37")
    version("00.32", sha256="ef1c1ebb61e6c8eb79dcaf5633d379cda36439792a6e5ed61e3bf11a1166295c")
    version("00.31", sha256="6a4b191add1ae1637b75f95da4dd56db8139c8dcf4504897d3f20e4d6d98d528")
    version("00.16", sha256="98507bf7adfe7b7ddfbfb043ef40c5c3eed55b3818be0c62766b759f06fc0b59")
    version("00.15", sha256="90bed72a1a2924132171d108799698602a28a4143ca2234d0ee988d80bd60d83")
    version("00.14", sha256="fc8c12331e2dcaaa0d5063dd86ae8b65f1221d1505ddb14a4490e6f23019d510")

    depends_on("castxml")
    depends_on("py-pygccxml")

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        mkdirp("%s/SRProxy" % self.prefix.include)
        copy(join_path(self.stage.source_path, "gen_srproxy"), self.prefix.bin)
        copy(join_path(self.stage.source_path, "*.h"), "%s/SRProxy" % self.prefix.include)
        copy(join_path(self.stage.source_path, "*.cxx"), "%s/SRProxy" % self.prefix.include)

    def setup_dependent_build_env(self, spack_env, dspec):
        spack_env.set("SRPROXY_DIR", self.prefix)
