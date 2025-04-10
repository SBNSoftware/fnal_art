# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class GoogleBenchmark(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/google/benchmark/"
    url = "https://github.com/google/benchmark/archive/v1.5.0.tar.gz"

    maintainers = ['marcmengel']

    version("1.5.2", sha256="dccbdab796baa1043f04982147e67bb6e118fe610da2c65f88912d73987e700c")
    version("1.5.1", sha256="23082937d1663a53b90cb5b61df4bcc312f6dee7018da78ba00dd6bd669dfef2")

    depends_on("googletest")

    def patch(self):
        filter_file(
            r"#include <numeric>", 
            "#include <numeric>\n#include <limits>",
            "src/benchmark_register.cc",
        )
        filter_file(
            r"add_cxx_compiler_flag\(-std=c\+\+11\)",
            "",
            "CMakeLists.txt"
        )

    def cmake_args(self):
        args = [self.define("BENCHMARK_ENABLE_TESTING", "OFF")]
        return args
