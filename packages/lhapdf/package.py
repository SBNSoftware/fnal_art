# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack import *
from spack.package import *


class Lhapdf(AutotoolsPackage):

    homepage = "https://www.hepforge.org/lhapdf"
    url = "https://lhapdf.hepforge.org/downloads/?f=lhapdf-5.9.1.tar.gz"

    version("6.5.4", sha256="2443a4b32cc3b0597c8248bd6e25703ace9c91a7a253c5f60b1b5428ef9c869e")
    version("6.5.3", sha256="57435cd695e297065d53e69bd29090765c934936b6a975ff8c559766f2230359")
    version("6.3.0", sha256="ed4d8772b7e6be26d1a7682a13c87338d67821847aa1640d78d67d2cef8b9b5d")
    version("6.2.3", sha256="d6e63addc56c57b6286dc43ffc56d901516f4779a93a0f1547e14b32cfd82dd1")

    def url_for_version(self, version):
        # between 5.x and 6.x they went to upper case names in the URLs
        if str(version)[0] < "6":
            urlf = "https://lhapdf.hepforge.org/downloads/?f=lhapdf-%s.tar.gz"
        else:
            urlf = "https://lhapdf.hepforge.org/downloads/?f=LHAPDF-%s.tar.gz"
        return urlf % version

    version("5.9.1", sha256="86b9b046d7f25627ce2aab6847ef1c5534972f4bae18de98225080cf5086919c")

    def patch(self):
        if os.path.exists("./config/config.sub"):
            os.remove("./config/config.sub")
            install(
                os.path.join(os.path.dirname(__file__), "../../config/config.sub"),
                "./config/config.sub",
            )
        if os.path.exists("./config/config.guess"):
            os.remove("./config/config.guess")
            install(
                os.path.join(os.path.dirname(__file__), "../../config/config.guess"),
                "./config/config.guess",
            )

    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("pdfsets")
    depends_on("python")
    depends_on("gettext",type="build")
    
    def configure_args(self):
        return ("--enable-low-memory", "--disable-pyext", "--disable-octave")

    @run_after("install")
    def link_pdfs(self):
        mkdirp(os.path.join(self.spec.prefix.share, "lhapdf/PDFsets"))
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
            os.symlink(
                "{0}/PDFsets/{1}".format(self.spec["pdfsets"].prefix, pdf),
                "{0}/lhapdf/PDFsets/{1}".format(self.spec.prefix.share, pdf),
            )

    @run_after("install")
    def copy_examples(self):
        with working_dir(self.stage.source_path):
            install_tree("examples", self.prefix.examples)
        with working_dir(self.prefix.examples):
            for f in glob.glob("Makefile.*"):
                os.remove(f)
            for f in glob.glob("*.py"):
                os.remove(f)

    def setup_build_environment(self, spack_env):
        cxxstd_flag = (
            ""
            if self.spec.variants["cxxstd"].value == "default"
            else "cxx{0}_flag".format(self.spec.variants["cxxstd"].value)
        )
        spack_env.append_flags("CXXFLAGS", getattr(self.compiler, cxxstd_flag))
