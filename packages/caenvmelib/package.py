# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Caenvmelib(MakefilePackage):
    """CAEN VME interface library"""

    homepage = "https://www.caen.it/products/caenvmelib-library/"
    url = "https://scisoft.fnal.gov/scisoft/reference_tarballs/CAENVMELib-v4.0.1.tgz"

    version("4.0.2", sha256="9049579e93fe074d8b8b91c1e58bd5ee6b48e21ffc28c20c60e935c747ab577f")
    version("4.0.1", sha256="e3e5d9950fd92a58eca0997ed09f5f14b50a1c6fbbc60d7d71c909ab31fe84d2")
    version("3.4.4", sha256="31273b99eb059d209721a82f20b74986c244a3920188e4156a44caff9e3a7c90")

    def url_for_version(self, version):
        url = "https://scisoft.fnal.gov/scisoft/reference_tarballs/CAENVMELib-v{0}.tgz"
        return url.format(version)

    depends_on("libusb")
    depends_on("ncurses", when="+sample")

    variant("sample", default=False, description="Build the sample application")

    def edit(self, spec, prefix):
        if "+sample" in self.spec:
            makefile = FileFilter("sample/Makefile")
            makefile.filter(r'^\s*CC\s*=.*',  'CC = ' + spack_cc)
            makefile.filter(r'^\s*INCLUDEDIR\s*=(.*)', r'INCLUDEDIR = \1 ' + spec["ncurses"].headers.include_flags)
            makefile.filter(r'^\s*DEPLIBS\s*=(.*)', 'DEPLIBS = -L' + prefix.lib + ' ' + spec["ncurses"].libs.ld_flags + r' \1')
            makefile = FileFilter("sampleio/Makefile")
            makefile.filter(r'^\s*CC\s*=.*',  'CC = ' + spack_cc)
            makefile.filter(r'^\s*CFLAGS\s*=(.*)', r'CFLAGS = \1 -I../include')
            makefile.filter(r'^\s*LDFLAGS\s*=(.*)', 'LDFLAGS = -L' + prefix.lib + r' \1')
    
    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        install_tree("include", prefix.include)

        if self.spec.target.family == "aarch64":
            install_tree("lib/arm64", prefix.lib)
        elif self.spec.target.family == "x86":
            install_tree("lib/x86", prefix.lib)
        else:
            install_tree("lib/x64", prefix.lib)  
        
        libs = find(prefix.lib, "libCAENVME*")
        print(libs)
        for lib in libs:
            symlink(lib, prefix.lib + "/libCAENVME.so")

        mkdirp(prefix + "/doc")
        install("*.txt", prefix + "/doc")

        install_tree("sample", prefix + "/sample")
        install_tree("sampleio", prefix + "/sampleio")
        if "+sample" in self.spec:
            # Have to make() here since it depends on the library being installed
            with working_dir("sample"):
                make()
            with working_dir("sampleio"):
                make()
            mkdirp(prefix.bin)
            install("sample/CAENVMEDemo", prefix.bin + "/CAENVMEDemo")
            install("sampleio/IODemo", prefix.bin + "/IODemo")
