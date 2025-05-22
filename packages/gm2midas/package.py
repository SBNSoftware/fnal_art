# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob
import os

from spack.package import *

try:
    from spack.build_systems.makefile import MakefileBuilder as builder
except ImportError:
    from spack.build_systems.makefile import MakefilePackage as builder


#
# works with build_directory() below to let us run the
# stage (build, install, etc.) in each subdirectory, and
# try a second time if it seems to fail the first time
#
def subdir_decorator(f):
    def repl(self, *args):

        save = self.build_directory
        with working_dir(save):
            subdirlist = glob.glob("*")
            subdirlist.sort(reverse=True)
            for d in subdirlist:
                if d != "doc" and os.path.exists(os.path.join(d, "Makefile")):
                    self.build_subdir = d
                    try:
                        f(self, *args)
                    except Exception:
                        f(self, *args)
        self.build_subdir = None

    return repl


class Gm2midas(MakefilePackage):
    """Gm2 experiment tracking code"""

    homepage = "https://redmine.fnal.gov/projects/gm2midas"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2midas.v9_60_00.tbz2"
    git_base = "https://cdcvs.fnal.gov/projects/gm2midas"
    version("spack_branch", branch="feature/mengel_spack", git=git_base, get_full_repo=True)

    def url_for_version(self, version):
        return (
            "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2midas.v%s.tbz2"
            % version.underscored
        )

    variant("cxxstd", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("root", type=("build", "run"))
    depends_on("zlib", type=("build", "run"))
    depends_on("openssl", type=("build", "run"))
    depends_on("libusb", type=("build", "run"))

    @property
    def build_directory(self):
        if getattr(self, "build_subdir", None):
            return os.path.join(self.stage.source_path, self.build_subdir)
        else:
            return self.stage.source_path

    def setup_build_environment(self, env):
        env.set("PREFIX", self.prefix)
        env.set("ROMESYS", self.stage.source_path + "/rome")
        env.set("MSCB_LDFLAGS", "-lusb-1.0 -L{0}".format(self.spec["libusb"].prefix.lib))
        env.set("SYSBIN_DIR", self.prefix.bin)
        env.set("SYSLIB_DIR", self.prefix.lib)
        env.set("SYSINC_DIR", self.prefix.inc)

    def patch(self):
        filter_file(
            "#include <typeinfo>",
            "#include <typeinfo>\nusing std::type_info;",
            "rome/include/ROMEUtilities.h",
        )
        filter_file("LIBS  = -lusb-1.0", "LIBS = ${MSCB_LDFLAGS}", "mscb/Makefile")
        filter_file("mkdir", "mkdir -p", "midas/Makefile")

    build = subdir_decorator(builder.build)

    def install(self, spec, prefix):
        self.build_subdir = "midas"
        with working_dir(self.build_directory):
            make("install")

    check = subdir_decorator(builder.check)
