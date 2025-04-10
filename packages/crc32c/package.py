# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Crc32c(CMakePackage):
    """
    This project collects a few CRC32C implementations under an umbrella
    that dispatches to a suitable implementation based on the host computer's
    hardware capabilities.

    CRC32C is specified as the CRC that uses the iSCSI polynomial in RFC 3720.
    The polynomial was introduced by G. Castagnoli, S. Braeuer and M. Herrmann.
    CRC32C is used in software such as Btrfs, ext4, Ceph and leveldb.
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/google/crc32c/archive/1.0.6.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version("1.1.1", sha256="a6533f45b1670b5d59b38a514d82b09c6fb70cc1050467220216335e873074e8")
    version("1.1.0", sha256="49de137bf1c2eb6268d5122674f7dd1524b9148ba65c7b85c5ae4b9be104a25a")

    # FIXME: Add dependencies if required.

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD=17",
            "-DCRC32C_BUILD_TESTS=OFF",
            "-DCRC32C_BUILD_BENCHMARKS=OFF",
            "-DCRC32C_USE_GLOG=OFF",
        ]
        return args
