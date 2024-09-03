# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class GenieXsec(Package):
    """Data files used by genie."""

    version("3.04.00", sha256="fb4dc9badd1771c92fabbf818b33544006e8b60c7fb0f33d5288a66d93bd19ea", 
             url="https://scisoft.fnal.gov/scisoft/packages/genie_xsec/v3_04_00/genie_xsec-3.04.00-noarch-G1810a0211a-k250-e1000.tar.bz2")

    version("2.12.10", "2cae8b754a9f824ddd27964d11732941fd88f52f0880d7f685017caba7fea6b7", 
             expand=False, url="file://" + os.path.dirname(__file__) + "/../../config/junk.xml")

    # tune_name values are designed to line up with the ups setup command
    # when setting the environment variable, we change to match typical
    # genie tune format
    variant(
        "tune_name",
        default="AR2320i00000-k250-e1000",
        multi=False,
        values=(
            "AR2320i00000-k250-e1000",
            "G1801a00000-k250-e1000",
            "G1802a00000-k250-e1000",
            "G1810a0211a-k250-e1000",
            "G1810a0211b-k250-e1000",
            "G2111a00000-k250-e1000",
            "GDNu2001a00000-k120-e200",
            "N1810j0211a-k250-e1000"
        ),
        when="@3.0:",
        description="Name of genie xsec tune set to install.",
    )

    urlbase_2 = ("https://scisoft.fnal.gov/scisoft/packages/genie_xsec/v2_12_10/genie_xsec-2.12.10-noarch-")
    urlbase_3 = ("https://scisoft.fnal.gov/scisoft/packages/genie_xsec/v3_04_00/genie_xsec-3.04.00-noarch-")

    resource(
        name="AR2320i00000-k250-e1000",
        placement="AR2320i00000-k250-e1000",
        when="tune_name=AR2320i00000-k250-e1000",
        url=urlbase_3 + "AR2320i00000-k250-e1000.tar.bz2",
        sha256="13cc9d740c170af9033623049162eeff0fb0b68156122d380aa3262e92e9f61f",
        )

    resource(
        name="G1801a00000-k250-e1000",
        placement="G1801a00000-k250-e1000",
        when="tune_name=G1801a00000-k250-e1000",
        url=urlbase_3 + "G1801a00000-k250-e1000.tar.bz2",
        sha256="f222ff56360c9c221e8f793a9c09ddbe6578dbbaa9031b3b3a49cb5ec186595d",
        )

    resource(
        name="G1802a00000-k250-e1000",
        placement="G1802a00000-k250-e1000",
        when="tune_name=G1802a00000-k250-e1000",
        url=urlbase_3 + "G1802a00000-k250-e1000.tar.bz2",
        sha256="d7189bd6c3933b3017c83fafddb84d57b48414632b577835e49babec8537ab6e",
        )

    resource(
        name="G1810a0211a-k250-e1000",
        placement="G1810a0211a-k250-e1000",
        when="tune_name=G1810a0211a-k250-e1000",
        url=urlbase_3 + "G1810a0211a-k250-e1000.tar.bz2",
        sha256="fb4dc9badd1771c92fabbf818b33544006e8b60c7fb0f33d5288a66d93bd19ea",
        )

    resource(
        name="G1810a0211b-k250-e1000",
        placement="G1810a0211b-k250-e1000",
        when="tune_name=G1810a0211b-k250-e1000",
        url=urlbase_3 + "G1810a0211b-k250-e1000.tar.bz2",
        sha256="a1031e49ac8ac426074f247d91b2c886edaf7c4fef13993fe69aad92ad698c34",
        )

    resource(
        name="G2111a00000-k250-e1000",
        placement="G2111a00000-k250-e1000",
        when="tune_name=G2111a00000-k250-e1000",
        url=urlbase_3 + "G2111a00000-k250-e1000.tar.bz2",
        sha256="ae159887772a54891fc4bddb189ab108d74c4a48db68c13ed7166524e8797590",
        )

    resource(
        name="GDNu2001a00000-k120-e200",
        placement="GDNu2001a00000-k120-e200",
        when="tune_name=GDNu2001a00000-k120-e200",
        url=urlbase_3 + "GDNu2001a00000-k120-e200.tar.bz2",
        sha256="69146aacc6c55bdc5c519e917e48ea005d160824bf960d17734e9c7c6d85b6cb",
        )

    resource(
        name="N1810j0211a-k250-e1000",
        placement="N1810j0211a-k250-e1000",
        when="tune_name=N1810j0211a-k250-e1000",
        url=urlbase_3 + "N1810j0211a-k250-e1000.tar.bz2",
        sha256="79e7ecd8d0dc577efb525831b90eb2f650c0cdd7fe5cd17e3ea610a686248e33",
        )

    variant(
        "xsec_name",
        default="DefaultPlusMECWithNC",
        multi=False,
        values=(
            "AltPion",
            "DefaultPlusMECWithNC",
            "DefaultPlusValenciaMEC",
            "EffSFTEM",
            "LocalFGNievesQEAndMEC",
            "ValenciaQEBergerSehgalCOHRES",
        ),
        when="@:3.0",
        description="Name of genie xsec set to install.",
    )

    resource(
        name="AltPion",
        placement="AltPion",
        when="xsec_name=AltPion",
        url=urlbase_2 + "AltPion.tar.bz2",
        sha256="49c4c5332c96edc4147e8cacd5b68e8dd89737e205741a21bc75a5ba18b967c4",
    )
    resource(
        name="DefaultPlusMECWithNC",
        placement="DefaultPlusMECWithNC",
        when="xsec_name=DefaultPlusMECWithNC",
        url=urlbase_2 + "DefaultPlusMECWithNC.tar.bz2",
        sha256="7c57caa96c319ad8007253e2a81c6ffcc4dcc6d0923dabbf7b8938d8363ac621",
    )
    resource(
        name="DefaultPlusValenciaMEC",
        placement="DefaultPlusValenciaMEC",
        when="xsec_name=DefaultPlusValenciaMEC",
        url=urlbase_2 + "DefaultPlusValenciaMEC.tar.bz2",
        sha256="fe1b584e7014bba6c4cba5646e1031f344e9efbf799a2aa26b706e28c40a4481",
    )
    resource(
        name="EffSFTEM",
        placement="EffSFTEM",
        when="xsec_name=EffSFTEM",
        url=urlbase_2 + "EffSFTEM.tar.bz2",
        sha256="b6365f1a150b90b79788f51b084a1dce7432d8ba10b7faa03ade3f6d558c82f6",
    )
    resource(
        name="LocalFGNievesQEAndMEC",
        placement="LocalFGNievesQEAndMEC",
        when="xsec_name=LocalFGNievesQEAndMEC",
        url=urlbase_2 + "LocalFGNievesQEAndMEC.tar.bz2",
        sha256="5f02d7efa46ef42052834d80b6923b41e502994daaf6037dad9793799ad4b346",
    )
    resource(
        name="ValenciaQEBergerSehgalCOHRES",
        placement="ValenciaQEBergerSehgalCOHRES",
        when="xsec_name=ValenciaQEBergerSehgalCOHRES",
        url=urlbase_2 + "ValenciaQEBergerSehgalCOHRES.tar.bz2",
        sha256="3e7c117777cb0da6232df1e1fe481fdb2afbfe55639b0d7b4ddf8027954ed1fa",
    )

    def install(self, spec, prefix):
        if(self.version >= Version("3.0")):
            val = spec.variants["tune_name"].value
            comb_str = val.split(':')[0].split('-')[0]
            tune_str = comb_str[:3]+"_"+comb_str[3:6]+"_"+comb_str[6:8]+"_"+comb_str[8:]

            install_tree(
                "{0}/{2}/v{1}/NULL/{2}".format(self.stage.source_path, self.version.underscored, val),
                "{0}/v{1}/NULL/{2}".format(prefix, self.version.underscored, val),
            )
        elif(self.version < Version("3.0")):
            val = spec.variants["xsec_name"].value
            install_tree(
                "{0}/{2}/v{1}/NULL/{2}".format(self.stage.source_path, self.version.underscored, val),
                "{0}/{1}".format(prefix, val),
            )

    def setup_run_environment(self, run_env):
        if(self.version >= Version("3.0")):
            val = self.spec['genie-xsec'].variants['tune_name'].value
            data_str = "{0}/v{1}/NULL/{2}/data".format(self.spec['genie-xsec'].prefix, self.version.underscored, val)
            raw_str = self.spec['genie-xsec'].variants['tune_name'].value
            comb_str = raw_str.split(':')[0].split('-')[0]
            tune_str = comb_str[:-8]+"_"+comb_str[-8:-5]+"_"+comb_str[-5:-3]+"_"+comb_str[-3:] 

            run_env.set("GENIEXSECPATH", data_str)
            run_env.set("GENIEXSECFILE", data_str+"/gxspl-NUsmall.xml")
            run_env.set("GXMLPATH", data_str)
            run_env.set("GENIE_XSEC_TUNE", tune_str)
            run_env.set("GENIE_XSEC_GENLIST", "Default")
            run_env.set("GENIE_XSEC_KNOTS", "250")
            run_env.set("GENIE_XSEC_EMAX", "1000.0")
