# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

from llnl.util import filesystem

from spack import *


class Genie(AutotoolsPackage):
    """GENIE is an international collaboration of scientists that plays the
    leading role in the development of comprehensive physics models for
    the simulation of neutrino interactions, and performs a highly-developed
    global analysis of neutrino scattering data."""

    homepage = "https://www.genie-mc.org"
    url = "https://github.com/GENIE-MC/Generator/archive/R-3_00_06.tar.gz"

    def url_for_version(self, version):
        return "https://github.com/GENIE-MC/Generator/archive/R-{0}.tar.gz".format(
            version.underscored
        )

    version("3.04.02", sha256="c5935aea86d2ba9897ab55bb581622c561575957d19e572691d3bc0833ed9512", preferred=True)
    version("3.04.00", sha256="72cf8a119cc59d03763b11afad1a82c0974a06677bf1c154b7c2a90d9f1529c1")
    version("3.00.06", sha256="ab56ea85d0c1d09029254365bfe75a1427effa717389753b9e0c1b6c2eaa5eaf")
    version("3.00.04", sha256="53f034618fef9f7f0e17d1c4ed72743e4bba590e824b795177a1a8a8486c861e")
    version("3.00.02", sha256="34d6c37017b2387c781aea7bc727a0aac0ef45d6b3f3982cc6f3fc82493f65c3")
    version("3.0.0b4", sha256="41100dd5141a7e2c934faaaf22f244deda08ab7f03745976dfed0f31e751e24e")
    version("3.00.00", sha256="3953c7d9f1f832dd32dfbc0b9260be59431206c204aec6ab0aa68c01176f2ae6")

    # parallel = False

    resource(
        name="reweight",
        url="https://github.com/GENIE-MC/Reweight/archive/R-1_00_02.tar.gz",
        sha256="58d5ad9c7f2bb3015be506bf40fe7b9e12e8f4ae7f2223cbebb568adb7e8fb19",
        placement="Reweight",
        when="@3.00.02:3.00.05",
    )
    resource(
        name="reweight",
        url="https://github.com/GENIE-MC/Reweight/archive/R-1_00_06.tar.gz",
        sha256="58d5ad9c7f2bb3015be506bf40fe7b9e12e8f4ae7f2223cbebb568adb7e8fb19",
        placement="Reweight",
        when="@3.00.06:3.03.99",
    )
    resource(
        name="reweight",
        url="https://github.com/GENIE-MC/Reweight/archive/R-1_02_02.tar.gz",
        sha256="741b323381079d0764b14095b12a16049930cbdfac182110fdda3c3263fb37b3",
        placement="Reweight",
        when="@3.04.00:",
    )


    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("lhapdf", default=True) 

    # Use mainline spack gettext for lhapdf
    depends_on("lhapdf" , when="+lhapdf")

    # Issues caused by default root cxxstd being 11
    depends_on("root @6.24.08:6.28.12 +pythia6 cxxstd=14", when="cxxstd=14")
    depends_on("root @6.24.08:6.28.12 +pythia6 cxxstd=17", when="cxxstd=17")
    depends_on("root @6.24.08:6.28.12 +pythia6 cxxstd=17", when="cxxstd=default")
    depends_on("root @6.24.08:6.28.12 +pythia6 cxxstd=20", when="cxxstd=20")

    depends_on("pythia6+root")
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("gsl")

    patch("patch/genie-r21210.patch", when="@2_12_10")
    patch("patch/genie-r30006.patch", when="@3.00.06")

    patch("patch/sles-cnl.patch", when="platform=cray")
    patch("patch/root_subdir.patch")

    patch("patch/GENIE-Generator.patch", when="@3.04.02")
    patch("patch/GENIE-Reweight.patch", when="@3.04.02", level=0)

    # @when("os=almalinux9") patch should be applied on polaris too
    def patch(self):
        filter_file(r'-lnsl','','src/make/Make.include')

    @property
    def build_targets(self):
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        args = [
            "GOPT_WITH_CXX_USERDEF_FLAGS=-g -fno-omit-frame-pointer {0}".format(cxxstdflag),
            "all",
        ]
        return args

    def configure_args(self):
        args = [
            "--enable-rwght",
            "--enable-fnal",
            "--enable-atmo",
            "--enable-event-server",
            "--enable-nucleon-decay",
            "--enable-neutron-osc",
            "--enable-vle-extension",
            "--with-pythia6-lib={0}".format(self.spec["pythia6"].prefix.lib),
            "--with-libxml2-inc={0}/libxml2".format(self.spec["libxml2"].prefix.include),
            "--with-libxml2-lib={0}".format(self.spec["libxml2"].prefix.lib),
            "--with-log4cpp-inc={0}".format(self.spec["log4cpp"].prefix.include),
            "--with-log4cpp-lib={0}".format(self.spec["log4cpp"].prefix),
            "--with-optimiz-level=O3",
        ]
        if self.spec.satisfies("^lhapdf@6:"):
            args.extend(
                [
                    "--enable-lhapdf6",
                    "--with-lhapdf6-lib={0}".format(self.spec["lhapdf"].prefix.lib),
                    "--with-lhapdf6-inc={0}".format(self.spec["lhapdf"].prefix.include),
                ]
            )
        elif self.spec.satisfies("^lhapdf@5:"):
            args.extend(
                [
                    "--enable-lhapdf5",
                    "--with-lhapdf5-lib={0}".format(self.spec["lhapdf"].prefix.lib),
                    "--with-lhapdf5-inc={0}".format(self.spec["lhapdf"].prefix.include),
                ]
            )
        elif self.spec.satisfies("^lhapdf"):
            args.extend(
                [
                    "--enable-lhapdf",
                    "--with-lhapdf-lib={0}".format(self.spec["lhapdf"].prefix.lib),
                    "--with-lhapdf-inc={0}".format(self.spec["lhapdf"].prefix.include),
                ]
            )
        return args

    @run_before("configure")
    def add_to_configure_env(self):
        inspect.getmodule(self).configure.add_default_env("GENIE", self.stage.source_path)
        inspect.getmodule(self).configure.add_default_env(
            "GENIE_REWEIGHT", "{0}/Reweight".format(self.stage.source_path)
        )
        inspect.getmodule(self).configure.add_default_env(
            "LD_LIBRARY_PATH", "{0}/lib".format(self.stage.source_path)
        )

    @run_before("build")
    def add_to_make_env(self):
        inspect.getmodule(self).make.add_default_env("GENIE", self.stage.source_path)
        inspect.getmodule(self).make.add_default_env(
            "GENIE_REWEIGHT", "{0}/Reweight".format(self.stage.source_path)
        )
        inspect.getmodule(self).make.add_default_env(
            "LD_LIBRARY_PATH", "{0}/lib".format(self.stage.source_path)
        )

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make(*self.build_targets)
        with working_dir("{0}/Reweight".format(self.stage.source_path)):
            make(*self.build_targets)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.lib64)
        mkdirp(prefix.include)
        mkdirp(prefix.src)
        mkdirp(prefix.config) # necessary for tune functionality
        mkdirp(prefix.data) # necessary for PDG library lookup

        with working_dir(self.build_directory):
            make("install")
        with working_dir("{0}/Reweight".format(self.stage.source_path)):
            make("install")

    @run_after("install")
    def install_required_src(self):
        # Install things from the source tree that are required.
        filesystem.install_tree(
            os.path.join(self.stage.source_path, "src", "scripts"),
            os.path.join(self.prefix, "src", "scripts"),
        )
        src_make_dir = os.path.join(self.prefix, "src", "make", "")
        config_dir = os.path.join(self.prefix, "config", "")
        data_dir = os.path.join(self.prefix, "data", "")
        # filesystem.mkdirp(src_make_dir)
        filesystem.install_tree(os.path.join(self.stage.source_path, "src", "make"), src_make_dir)
        filesystem.install_tree(os.path.join(self.stage.source_path, "config"), config_dir)
        filesystem.install_tree(os.path.join(self.stage.source_path, "data"), data_dir)

    def setup_build_environment(self, spack_env):
        spack_env.set("ROOT_INCLUDE_PATH", os.path.join(self.stage.source_path, "src"))
        spack_env.set("GENIE_VERSION", "v{0}".format(self.version.underscored))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.set("GENIE", self.prefix)
        run_env.set("GENIE_VERSION", "v{0}".format(self.version.underscored))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("ROOT_INCLUDE_PATH", "{0}/GENIE".format(self.prefix.include))

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("GENIE", self.prefix)
        spack_env.set("GENIE_VERSION", "v{0}".format(self.version.underscored))
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("ROOT_INCLUDE_PATH", "{0}/GENIE".format(self.prefix.include))
        spack_env.append_path("LD_LIBRARY_PATH", self.prefix.lib)

    @run_after("install")
    def version_file(self):
        f = open(join_path(self.spec.prefix, "VERSION"), "w")
        f.write(str(self.version))
        f.close()
