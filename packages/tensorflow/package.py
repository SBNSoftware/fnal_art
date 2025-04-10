# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Tensorflow(Package):
    """An Open Source Machine Learning Framework for Everyone"""

    homepage = "https://tensorflow.org"
    url = "https://github.com/tensorflow/tensorflow/archive/v1.12.0.tar.gz"

    version("1.12.0", sha256="3c87b81e37d4ed7f3da6200474fa5e656ffd20d8811068572f43610cae97ca92")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("patch/tensorflow.patch", level=2, when="cxxstd=14")
    patch("patch/tensorflow_cxx17.patch", level=2, when="cxxstd=17")

    depends_on("protobuf")

    def patch(self):
        if "cxxstd=17" in self.spec:
            install(
                os.path.join(os.path.dirname(__file__), "patch/build_all_linux_cxx17.sh"),
                "tensorflow/contrib/makefile/build_all_linux.sh",
            )
        else:
            install(
                os.path.join(os.path.dirname(__file__), "patch/build_all_linux.sh"),
                "tensorflow/contrib/makefile/build_all_linux.sh",
            )

        install(os.path.join(os.path.dirname(__file__), "patch/install_all.sh"), "install_all.sh")
        install(
            os.path.join(os.path.dirname(__file__), "patch/rename_eigen.sh"),
            "tensorflow/contrib/makefile/rename_eigen.sh",
        )

    def install(self, spec, prefix):
        build_script = Executable("./tensorflow/contrib/makefile/build_all_linux.sh")
        build_script.add_default_env("TENSORFLOW_FQ_DIR", "{0}".format(prefix))
        build_script.add_default_env("TENSORFLOW_FQ_DIR", "{0}".format(spec["protobuf"].prefix))
        build_script()
        install_script = Executable("./install_all.sh")
        install_script.add_default_env("TENSORFLOW_FQ_DIR", "{0}".format(prefix))
        install_script()

    def setup_build_environment(self, spack_env):
        spec = self.spec
        spack_env.set("TENSORFLOW_FQ_DIR", "{0}".format(self.prefix))
        spack_env.set("PROTOBUF_FQ_DIR", "{0}".format(spec["protobuf"].prefix))
