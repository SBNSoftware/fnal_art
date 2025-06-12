# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack.package import *


class Caendigitizer(MakefilePackage):
    """CAEN Digitizer software library"""

    homepage = "https://www.caen.it/products/caendigitizer-library/"
    url = "https://scisoft.fnal.gov/scisoft/reference_tarballs/CAENDigitizer-v2.17.3.tgz"

    version("2.17.3", sha256="8337552f390c28f6a9dffed464d668eec07c83d5f2b68cabb77d957ef8592cf6")

    def url_for_version(self, version):
        url = "https://scisoft.fnal.gov/scisoft/reference_tarballs/CAENDigitizer-v{0}.tgz"
        return url.format(version)

    depends_on("caencomm")
    depends_on("caenvmelib")

    variant("samples", default=False, description="Build the sample applications")

    def edit(self, spec, prefix):
        if "+samples" in self.spec:
            makefiles = find("samples", "Makefile")
            for file in makefiles:
                print(f"Patching file {file}")
                makefile = FileFilter(file)
                makefile.filter(r'^\s*CC\s*=.*',  'CC = ' + spack_cc)
                makefile.filter(r'^\s*INCLUDEDIR\s*=(.*)', r'INCLUDEDIR = \1 -I' + prefix.include)
                makefile.filter(r'^\s*DEPLIBS\s*=(.*)', 'DEPLIBS = -L' + prefix.lib + r' \1')

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

        libs = find(prefix.lib, "libCAENDigitizer*")
        print(libs)
        for lib in libs:
            symlink(lib, prefix.lib + "/libCAENDigitizer.so")

        mkdirp(prefix + "/doc")
        install("*.txt", prefix + "/doc")

        install_tree("samples", prefix + "/samples")
        if "+samples" in self.spec:
            mkdirp(prefix.bin)
            # Have to make() here since it depends on the library being installed
            dirs = FileList(find("samples", "Makefile")).directories
            for thisdir in dirs:
                with working_dir(thisdir):
                    make()
            sample_bins = find("samples", "*.bin")
            for sample_bin in sample_bins:            
                install(sample_bin, prefix.bin)
