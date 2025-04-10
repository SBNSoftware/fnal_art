# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class GoogleCloudCpp(CMakePackage):
    """This repository contains idiomatic C++ client libraries for the
    following Google Cloud Platform services.

    Google Cloud Bigtable [quickstart]
    Google Cloud Spanner [quickstart]
    Google Cloud Pub/Sub [quickstart]
    Google Cloud Storage [quickstart]
    """

    homepage = "https://github.com/googleapis/google-cloud-cpp/"
    url = "https://github.com/googleapis/google-cloud-cpp/archive/v1.24.0.tar.gz"

    maintainers = [ "marcmengel" ]

    version( "1.24.0", sha256="705992bbf5d86a5d5b4276fe249ca495bc0827f1835cb433f3f6be777072aa62")
    version( "1.23.0", sha256="914c9596ee9f271a4ba2de701388009d1f6a7eb0ea269d625aae06be1a51ee9e")
    version( "1.22.0", sha256="2f52dcc679a31e738c01fb68aa0fc966fe0be5322d1a4ec7e6337363281a4704")
    version( "1.21.0", sha256="14bf9bf97431b890e0ae5dca8f8904841d4883b8596a7108a42f5700ae58d711")

    depends_on("crc32c")
    depends_on("curl")
    depends_on("google-benchmark")
    depends_on("googletest +gmock")
    depends_on("grpc")
    depends_on("nlohmann-json")
    # depends_on('benchmark')
    depends_on("abseil-cpp")

    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("absl-make-unique.patch")

    def patch(self):
        # this file is missing an include for <thread> ...
        filter_file(
            r"namespace google \{",
            "#include <thread>\nnamespace google {",
            "google/cloud/bigtable/tests/data_integration_test.cc",
        )
        with (when("@:2.18.0 %gccc@13:")):
            filter_file(
                r"#include <vector>",
                "#include <vector>\n#include <cstdint>",
                "google/cloud/iam_bindings.h",
            )
            filter_file(
                r"#include <vector>",
                "#include <vector>\n#include <cstdint>",
                "google/cloud/storage/iam_policy.h",
            )
            filter_file(
                r"#include <string>",
                "#include <string>\n#include <cstdint>",
                "google/cloud/version.h",
            )

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

