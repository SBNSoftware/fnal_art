# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pdfsets(Package):
    """PDF sets used by Genie"""

    homepage = "https://genie.hepforge.org"
    url = "https://github.com/GENIE-MC/Generator/archive/R-2_8_6.tar.gz"

    version(
        "5.9.1",
        url="https://github.com/GENIE-MC/Generator/archive/R-2_8_6.tar.gz",
        sha256="310dc8e0d17a65e6b9773e398250703a3a6f94ceafe94f599ae0f7b3fecf7e6c",
    )
    version(
        "2.8.6",
        url="https://github.com/GENIE-MC/Generator/archive/R-2_8_6.tar.gz",
        sha256="310dc8e0d17a65e6b9773e398250703a3a6f94ceafe94f599ae0f7b3fecf7e6c",
    )

    resource(
        name="CT10.LHgrid",
        placement="CT10.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/CT10.LHgrid",
        expand=False,
        sha256="edd17727b3fbb93f2f1153f219ace7dc18d52eacae27d37a7e123ca4552d2b80",
    )
    resource(
        name="cteq61.LHgrid",
        placement="cteq61.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/cteq61.LHgrid",
        expand=False,
        sha256="d384a9edd4534d1ca70ea940234fd0286229337083ef5869edf432bac6083dfe",
    )
    resource(
        name="cteq61.LHpdf",
        placement="cteq61.LHpdf",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/cteq61.LHpdf",
        expand=False,
        sha256="0dacfd4d5518b2273ba80ae381af7d46eab4784e84312585f5f149f8fce759f0",
    )
    resource(
        name="GRV98lo.LHgrid",
        placement="GRV98lo.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/GRV98lo.LHgrid",
        expand=False,
        sha256="125e99d8d824705e4449cf4ec1b4410fd6bf1d0235e96316b5f37af7438dcda4",
    )
    resource(
        name="GRV98nlo.LHgrid",
        placement="GRV98nlo.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/GRV98nlo.LHgrid",
        expand=False,
        sha256="78e7b133ac1f1d5576aa688f98adb8b6e29feb15cbb58556c860cb7e183da647",
    )
    resource(
        name="GRVG0.LHgrid",
        placement="GRVG0.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/GRVG0.LHgrid",
        expand=False,
        sha256="a17a14488a6136d1b160656f75c330b47a30f7221f865614f99bc0e1968a76d6",
    )
    resource(
        name="GRVG1.LHgrid",
        placement="GRVG1.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/GRVG1.LHgrid",
        expand=False,
        sha256="359174502ae6c97a0050d472081cbfebc3ed8d0dc8f28a3bc06cf753241822ad",
    )
    resource(
        name="GRVPI0.LHgrid",
        placement="GRVPI0.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/GRVPI0.LHgrid",
        expand=False,
        sha256="de982111b99bd04ba3560715b12ff4fea37e35a5b491d78601847eb9adbd6a71",
    )
    resource(
        name="GRVPI1.LHgrid",
        placement="GRVPI1.LHgrid",
        url="https://www.hepforge.org/downloads/lhapdf/pdfsets/5.9.1/GRVPI1.LHgrid",
        expand=False,
        sha256="68c7f07fb1929ef2c0e68e5229d8ce57232446b483bdcd44db2b14204785cd9a",
    )

    def setup_build_environment(self, spack_env):
        spack_env.set("LHAPATH", "{0}/PDFsets".format(self.prefix))

    def setup_run_environment(self, run_env):
        run_env.set("LHAPATH", "{0}/PDFsets".format(self.prefix))

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LHAPATH", "{0}/PDFsets".format(self.spec.prefix))

    def install(self, spec, prefix):
        mkdirp("{0}/PDFsets".format(prefix))
        install(
            "data/evgen/pdfs/GRV98lo_patched.LHgrid",
            "{0}/PDFsets/GRV98lo_patched.LHgrid".format(prefix),
        )
        pdfs = [
            "CT10.LHgrid",
            "cteq61.LHgrid",
            "cteq61.LHpdf",
            "GRV98lo.LHgrid",
            "GRV98nlo.LHgrid",
            "GRVG0.LHgrid",
            "GRVG1.LHgrid",
            "GRVPI0.LHgrid",
            "GRVPI1.LHgrid",
        ]
        for pdf in pdfs:
            install("{0}/{1}".format(pdf, pdf), "{0}/PDFsets/{1}".format(prefix, pdf))
