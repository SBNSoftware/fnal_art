# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *


class IfdhcConfig(Package):
    """Config package for Data handling client code for intensity frontier experiments"""

    homepage = "https://github.com/fnal-fife/ifdhc"
    git_base = "https://github.com/fnal-fife/ifdhc.git"
    url = "https://github.com/fnal-fife/ifdhc/archive/refs/tags/v2_6_14.tar.gz"
    list_url = "https://github.com/fnal-fife/ifdhc/tags"

    version("2.8.0", sha256="189404744961ca049366369b71b783e57540cd4f6a45b86f0aed5f14c198d590")
    version("2.7.4", sha256="940dc661cfb5a1bf9bf7353b03b0fd732289a951ef99992327f29ce94f1cac9f")
    version("2.7.3", sha256="8a8caa1d14a0d39c8ccb96460b84cca51540f209535c62cd680243dc08d1db5f")
    version("2.7.2", sha256="036933c0443a4704f408aea83972954e2af6d933a7ffe61869ac4e6e6fd41256")
    version("2.7.1", sha256="4494d08c3a7927600bbcee56e65feb024b15e2d510328ec0d2cc0fcefc5cb6a7")
    version("2.7", sha256="5a4f7c94191bb657415a51c6d73d789f820999b68c8d9c65ec74c845321aa7e2")
    version("2.6.20", sha256="cd473b3331474a75f87c3251e08c69bb3b0a7c98f53171c5a380049bca1a0cc2")
    version("2.6.19", sha256="8ce4cb631fb1662e3146a1877e92677859cb2196cf90504e7b4a55811cc45b4b")
    version("2.6.18", sha256="c8d353ea648177802b2c2e87213a4b5cbffa62cd6b340bc3c6d574402955791c")
    version("2.6.17", sha256="d4d3614122099f386d9b4e570dcd058a9d6853c96a8ec6beafcbcb8cee4ebb02")
    version("2.6.14", sha256="df6d78b62ba074aac84281b021037319623e2bc4a90bfb46a7129ebdf3281ec1")
    version("2.6.8", sha256="3dc0fca76815424a72613df68520dafc08341c9f60c80a766bda647819212d87")
    version("2.6.6", sha256="8ba4929ecefa5720ea999e39671a48b56a65f5f44ff99f2f473f9cd47277051e")
    version("develop", git=git_base, branch="develop", get_full_repo=True)

    parallel = False

    def url_for_version(self, version):
        url = "https://github.com/fnal-fife/ifdhc/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    def install(self, a, b):
        instlist=[
                ['ifdh.cfg', ''], 
                ['ifdh/www_cp.sh', '/bin'],
                ['ifdh/auth_session.sh', '/bin'], 
                ['ifdh/decode_token.sh', '/bin'],
               ]
        mkdir(self.spec.prefix.bin)
        for fnpair in instlist:
            install("{0}/{1}".format( self.stage.source_path, fnpair[0]),
                    "{0}{1}".format( self.spec.prefix, fnpair[1]))
            tty.warn("installing {0}".format(fnpair[0]))

    def setup_build_environment(self, spack_env):
        spack_env.set("IFDHC_CONFIG_DIR", self.spec.prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.spec.prefix.bin)
        run_env.set("IFDHC_CONFIG_DIR", self.spec.prefix)
        # save for ifhdc setup_run_environment to use..
        os.environ["IFDHC_CONFIG_BIN"] = str(self.spec.prefix.bin)
