# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libpqxx(CMakePackage):
    """libpqxx, the C++ API to the PostgreSQL database management system."""

    homepage = "http://pqxx.org/development/libpqxx/"
    url = "https://github.com/jtv/libpqxx/archive/refs/tags/7.6.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['marcmengel']

    version("7.10.0", sha256="d588bca36357eda8bcafd5bc1f95df1afe613fdc70c80e426fc89eecb828fc3e")
    version("7.9.2", sha256="e37d5774c39f6c802e32d7f418e88b8e530404fb54758516e884fc0ebdee6da4")
    version("7.9.1", sha256="4fafd63009b1d6c2b64b8c184c04ae4d1f7aa99d8585154832d28012bae5b0b6")
    version("7.9.0", sha256="a1fafd5f6455f6c66241fca1f35f5cb603251580b99f9a0cf1b5d0a586006f16")
    version("7.8.1", sha256="0f4c0762de45a415c9fd7357ce508666fa88b9a4a463f5fb76c235bc80dd6a84")
    version("7.8.0", sha256="bc471d8d34588f820f38e19e1cc217f399212eef900416cf12f90fab293628af")
    version("7.7.5", sha256="c7dc3e8fa2eee656f2b6a8179d72f15db10e97a80dc4f173f806e615ea990973")
    version("7.7.4", sha256="65b0a06fffd565a19edacedada1dcfa0c1ecd782cead0ee067b19e2464875c36")
    version("7.7.3", sha256="11e147bbe2d3024d68d29b38eab5d75899dbb6131e421a2dbf9f88bac9bf4b0d")
    version("7.7.2", sha256="4b7a0b67cbd75d1c31e1e8a07c942ffbe9eec4e32c29b15d71cc225dc737e243")
    version("7.6.0", sha256="8194ce4eff3fee5325963ccc28d3542cfaa54ba1400833d0df6948de3573c118")
    version("7.6.0", sha256="8194ce4eff3fee5325963ccc28d3542cfaa54ba1400833d0df6948de3573c118")
    version("7.5.2", sha256="62e140667fb1bc9b61fa01cbf46f8ff73236eba6f3f7fbcf98108ce6bbc18dcd")
    version("7.5.1", sha256="16a3a4097a6772a9824ba584dbe5a1feee163ab954b94497358fe591eb236e3d")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("postgresql")

    def cmake_args(self):
        args = [
            "DPostgreSQL_TYPE_INCLUDE_DIR=%s" % self.spec["postgresql"].prefix.include,
            "DPostgreSQL_INCLUDE_DIR=%s" % self.spec["postgresql"].prefix.include,
            "DPostgreSQL_LIBRAY_DIR=%s" % self.spec["postgresql"].prefix.lib,
        ]
        return args
