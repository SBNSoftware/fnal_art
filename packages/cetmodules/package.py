# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cetmodules(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = "https://fnalssi.github.io/cetmodules/"
    git = "https://github.com/FNALssi/cetmodules.git"
    url = "https://github.com/FNALssi/cetmodules/archive/refs/tags/3.13.02.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]

    version("develop", branch="develop", get_full_repo=True)
    version("3.13.02", sha256="11bc4b55a3b07dfe1187d3f04c977caec9fb06d412ed50241f30507398cc7cac")
    version("3.19.02", sha256="214172a59f4c3875a5d7c2617b9f50ed471c86404d85e2e5c72cadf5b499cdc6")
    version("3.21.00", sha256="429ddecf2e905a6a3156c267005d17cd6e160533f28bcef0be40a9d0057e95e4")
    version("3.21.01", sha256="9f4b845f9ed09fb3a8ee7864ac487afd08a5b3e64abf394831ee927f91b08ebc")
    version("3.21.02", sha256="255d6d6c2455217734b208fc90919b90bc7c0f9a59a4706d329c642bff51f004")
    version("3.22.01", sha256="c72c47328adc0c95f905aae119c76d35513a0677f20163f0ef25a82bd0f72082")
    version("3.22.02", sha256="bbd6a80ab3c495e49b3545230c97ae880755a5f1d39b71d89f07297bf835e5da")
    version("3.24.01", sha256="6ef8b522b02298a787a318cda898deedc250cdd336dc3168fad934ef607b5916")
    version("3.25.00", sha256="9574d9f8e5757d79c11d6fb3b95c3227aa0028960733715c3e6b6b25a51ff5c5")

    variant(
        "versioned-docs", default=False, description="build versioned docs with a landing page"
    )
    variant("docs", default=False, when="~versioned-docs", description="build documentation")

    depends_on("cmake@3.20:", when="@3.03.00:", type=("build", "run"))
    depends_on("cmake@3.21:", when="@3.22.02:", type=("build", "run"))
    depends_on("cmake@3.22:", when="@3.23.00:", type=("build", "run"))

    with when("+versioned-docs") or when("+docs"):
        depends_on("git@2.22:", type="build")
        depends_on("py-sphinxcontrib-moderncmakedomain", type="build")
        depends_on("py-sphinx-design@0.2.0:", type="build")
        depends_on("py-sphinx@5:", type="build")

        with when("@3.23.00:"):
            depends_on("py-sphinxcontrib-moderncmakedomain@3.25:", type="build")
            depends_on("py-sphinx@6:", type="build")
            with when("+versioned-docs"):
                depends_on("py-sphinx-toolbox", type="build")
                depends_on("py-sphinxcontrib-jquery", type="build")

        with when("@:3.22.99"):
            depends_on("py-sphinx@:5", type="build")

    perl_deps = {
        "perl-data-dumper": ("build", "run"),
        "perl-json": ("build", "run"),
        "perl-list-moreutils": ("build", "run"),
        "perl-metacpan-client": ("build", "run"),
        "perl-path-tiny": ("build", "run"),
        "perl-readonly": ("build", "test", "run"),
        "perl-perl-tidy": ("build", "test", "run"),
        "perl-task-perl-critic": ("build", "test"),
    }

#    for pkg, types in perl_deps.items():
#        depends_on(pkg, type=types)

    conflicts("@:3.19.01", when="^cmake@3.24.0:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @run_before("cmake")
    def fix_fix_man(self):
        filter_file(r"exit \$status", "exit 0", "%s/libexec/fix-man-dirs" % self.stage.source_path)

    def cmake_args(self):
        spec = self.spec
        define = self.define
        options = ["--preset", "default"]
        if not any(
            [
                spec.variants[doc_opt].value
                for doc_opt in ("docs", "versioned-docs")
                if doc_opt in spec.variants
            ]
        ):
            options.append(define("BUILD_DOCS", False))
        elif spec.variants["versioned-docs"].value:
            options += [
                define(
                    f"{self.name}_SPHINX_DOC_PUBLISH_VERSION_BRANCH", spec.version
                ),
                define(
                    f"{self.name}_SPHINX_DOC_PUBLISH_ROOT",
                    join_path(self.stage.path, "doc_root"),
                ),
            ]
        return options
