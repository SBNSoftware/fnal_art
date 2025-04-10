# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os.path

from spack.package import *


class Pandora(CMakePackage):
    """PandoraPFA Multi-algorithm pattern recognition"""

    homepage = "https://github.com/PandoraPFA"

    version(
        "03.11.01",
        git="https://github.com/PandoraPFA/PandoraPFA",
        tag="v03-11-01",
        get_full_repo=True,
    )
    version(
        "03.16.00",
        git="https://github.com/PandoraPFA/PandoraPFA",
        tag="v03-16-00",
        get_full_repo=True,
    )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant(
       "monitoring",
       default=True,
       description="Enable PandoraMonitoring when building."
    )

    depends_on("root +opengl", when="+monitoring")
    depends_on("root ~opengl", when="~monitoring")

    depends_on("eigen")


    def patch(self):
        # Build larpandoracontent as part of pandora
        filter_file(
            'LArContent_version "v03_13_01"', 'LArContent_version "v03_14_05"', "CMakeLists.txt"
        )
        filter_file(
            'Eigen3_version "3.3.3"',
            'Eigen3_version "{0}"'.format(self.spec["eigen"].version),
            "CMakeLists.txt",
        )
        filter_file(
            r"            EXPORT_LIBRARY_DEPENDENCIES\((.*)\)",
            """
            CMAKE_POLICY( PUSH )
            CMAKE_POLICY( SET CMP0033 OLD )
            EXPORT_LIBRARY_DEPENDENCIES( \\1 )
            CMAKE_POLICY( POP )""",
            "cmakemodules/MacroPandoraGeneratePackageConfigFiles.cmake",
        )


    # apply patch to 3.16.00 (to clear warnings in newer compilers)
    # we have to apply our this patch *after* the initial
    # cmake run because that and then a "make" downloads the sources we
    # need to patch...`
    @run_after("cmake") 
    def patch_pandora(self):
        patch = which("patch") 
        make = which("make")
        if self.spec.variants['generator'].value == 'ninja':
            make = which("ninja")
        pdir = os.path.dirname(__file__)

        with when("@03.16.00"):
            with working_dir(self.build_directory):
                make("PandoraSDK", output="make-0.out", error="make-0.err", fail_on_error=False)

            with working_dir(self.stage.source_path):
                g = glob.glob("PandoraSDK-v*")
                if g:
                   gd = g[0]
                else:
                   gd = "PandoraSDK"
                filter_file(
                    '#include <vector>',
                    '#include <vector>\n#include <cstdint>',
                    gd + '/include/Pandora/PandoraInternal.h',
                )

            with working_dir(self.build_directory):
                make("LCContent","LArContent")

            with working_dir(self.build_directory):
                patch("-p0", "-t", "-i", 
                       os.path.join(pdir,"pandora-v03-16-00.patch"), fail_on_error=False)
                if self.spec.variants["monitoring"].value:
                    patch("-p0", "-t", "-i", 
                           os.path.join(pdir,"pandora-monitoring-v03-16-00.patch"), fail_on_error=False)

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCMAKE_CXX_FLAGS=-Wno-implicit-fallthrough -std=c++{0}".format(
                self.spec.variants["cxxstd"].value
            ),
            "-DCMAKE_MODULE_PATH={0}/etc/cmake".format(self.spec["root"].prefix),
            "-DPANDORA_MONITORING={0}".format("ON" if self.spec.variants["monitoring"].value else "OFF"),
            "-DLC_PANDORA_CONTENT=ON",
            "-DLAR_PANDORA_CONTENT=ON",
            "-DINSTALL_DOC=OFF",
            "-DEXAMPLE_PANDORA_CONTENT=OFF",
        ]
        return args


    @run_after("install")
    def install_modules(self):
        install_tree("cmakemodules", "{0}/cmakemodules".format(self.prefix))
        for f in glob.glob("{0}/*.cmake".format(self.prefix)):
            wrongp = "{0}/spack-src/cmakemodules".format(self.stage.path)
            rightp = "{0}/cmakemodules".format(self.prefix)
            filter_file(wrongp, rightp, f, backup=False)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("CMAKE_PREFIX_PATH", "{0}/cmakemodules".format(self.prefix))

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CMAKE_PREFIX_PATH", "{0}/cmakemodules".format(self.prefix))
