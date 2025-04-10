# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libb64(MakefilePackage):
    """A fast base-64 encoder/decoder in C++"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://libb64.sourceforge.net/"
    url = "https://sourceforge.net/projects/libb64/files/libb64/libb64/libb64-1.2.1.zip"

    maintainers = [
        "marcmengel",
    ]

    version("1.2.1", sha256="20106f0ba95cfd9c35a13c71206643e3fb3e46512df3e2efb2fdbf87116314b2")

    build_targets = ["clean", "all_src", "all"]
    parallel = False

    def install(self, spec, prefix):
        filter_file("BUFFERSIZE", "BUFSIZ", "include/b64/encode.h")
        filter_file("BUFFERSIZE", "BUFSIZ", "include/b64/decode.h")
        mkdirp(prefix.bin)
        mkdirp(prefix.lib.pkgconfig)
        mkdirp(prefix.include)
        install("src/*.a", prefix.lib)
        install("base64/base64", prefix.bin)
        install_tree("include", prefix.include)
        f = open("%s/libb64.pc" % prefix.lib.pkgconfig, "w")
        f.write(
            """prefix=%s
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
sharedlibdir=${libdir}
includedir=${prefix}/include

Name: libb64
Description: base64 encode/decode library
Version: %s
Requires:
Libs: -L${libdir} -lb64
Cflags: -I${includedir}/.

"""
            % (self.prefix, self.version)
        )
        f.close()
