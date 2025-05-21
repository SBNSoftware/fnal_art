# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
import spack.util.web
from spack.package import *


class Wibtools(CMakePackage):
    """Tools for communicating with the WIB hardware"""

    homepage = "https://github.com/SBNSoftware"
    url = "https://github.com/SBNSoftware/wibtools"
    git_base = "https://github.com/SBNSoftware/wibtools.git"
    list_url = "https://api.github.com/repos/SBNSoftware/wibtools/tags"

    version("1.08.00", sha256="1c496184d30f3c5aa633add614c6ccd517b9c46a7d128e6c2049fcbe445b2190")
    version("1.07.01", sha256="1db3bc7dc75b47e603e817bf978e88277c4f0b04d430d508efada44d934bc675")
    version("1.06.00", sha256="d7716683fed7742d2202b522499dd74507af442c2c7945d0d668f75590535464")
    version("1.05.00", sha256="11385f5d0148aa544a01730bf7076326d6301b5e2fe8499eafe66d10613beace")
    version("1.04.01", sha256="dc3c92a9569b93eb47ab126da8f483879a1cb68d8f87d7c77fa2b3f9356b6beb")
    version("1.04.00", sha256="660d2b9354ba527278412c8ce20d37c462b1067156f971c66ffc2d1d9564c9c6")
    version("1.03.00", sha256="136f3950d9a25d2b81d2eb7b44981d0e288b7fdf9223b9f7ad8379093450ca9b")
    version("1.02.01", sha256="bc1774e9df0099692ae42b068698712c17bd34b9dc66bd352972211cbc3b2024")
    version("1.02.00", sha256="a2cd80396e32e2db73442a8decadf74924bdf9b258ee0325843455d4915eb44e")
    version("1.01.00", sha256="48b19b70456a758b8866490fd9b751fc265f140b8fafd53d3f91709d5e7054ef")
    version("1.00.00", sha256="6f0b783fa4182a91e8d8ed4081f9b8c616c7e681ff0e5e19021a94610f319f40")
    version("0.05.00", sha256="390e5d6c242dca98f8220c392a61167656d86f2114d070a2d236d8af809fadd3")
    version("0.04.02", sha256="8588f1608a5c9686466a8414f488c2a7b447cbeb4e2484fa77e1cc6376def8e9")
    version("0.04.01", sha256="781135bb0d314913d20e8216e1f2182591aa21f6da3bf70601799b9dd703d289")
    version("0.04.00", sha256="214e4e177c5d92760014e613e1aadb9aad1052dea00a520e611d11f6502aae43")
    version("0.03.11", sha256="0495d8946e2862e607291c98ce36d041f778dfab435506b44b3678fcf73e9588")
    version("0.03.10", sha256="d506c02d373e8f2d0d52f1819177fe291e2662bd1c4dac5efc1c053df9a0cfd1")
    version("0.03.09", sha256="4c4ba12a6378c4627b86c541d1d176501882e039dcf4c6e6adb9dec793312b16")
    version("0.03.08", sha256="588e1ca7ab0ec731703eebe9094bf9a57acc4f94495c25336ed89cff932efa97")
    version("0.03.07", sha256="099e6cb860ca9f824e28c55003c9d7db7714cd198f5a485a4b7130d61e0cb063")
    version("0.03.06", sha256="23e3e06b82fa940c631811d706f0b06072aa934e7fb879bb5149cc9dacac9b7c")
    version("0.03.05", sha256="3d396178eab5ea8f02a373391ce8b4b195eb817305991535dcd18279e70533a5")
    version("0.03.04", sha256="7644816dbca695be969e5e0fe64569c34c1676c9d504f38344141100e19edc5a")
    version("0.03.03", sha256="0c7fedd5c815bbcbe7699bee9ec706d6b7f1e00f73f453da178fae8aaa690ecd")
    version("0.03.02", sha256="9efa2d1799cff79e639e6a32003bf713ca0fe95e7537984d6625b60162e808d7")
    version("0.03.01", sha256="aeb5013389aeb1c611c3bf82a7763ac6801ac99229659d5f95ca90e11dc753b8")
    version("0.03.00", sha256="4453ca21abd79654cf53fa170c198f4253e0eb54514dd7b5dacb4cb17d093fcf")
    version("0.02.00", sha256="15469f7103d2c65b0f868b21d7e652738845dcdb54ca95c05ef3be75607447e2")
    version("0.01.03", sha256="5985196dac09f13d5f2d9b10ddc5416aac8b5951e288db88f56dce086c5d6769")
    version("0.01.00", sha256="a180cc6dedfebc1f7cf4d51825babd294d67cf06b6e4b6973c65290abe0bde82")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("boost")
    depends_on("trace", type="build")
    depends_on("messagefacility")
    depends_on("cetmodules", type="build")
    
    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(spack.util.web.read_from_url(self.list_url, accept_content_type="application/json")[2])
                    if d["name"].startswith("v")
                ],
            )
        )

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
        ]
        return args

    def setup_run_environment(self, env):
        prefix = self.prefix
        env.set("WIBTOOLS_BIN", prefix.bin)
        env.set("WIB_ADDRESS_TABLE_PATH", prefix + "/tables")
        env.set("EIB_CONFIG_PATH", prefix + "/config")
