# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cosmosis(MakefilePackage):
    """CosmoSIS is a modular system for cosmological parameter estimation problems."""

    homepage = "https://bitbucket.org/joezuntz/cosmosis/wiki/Home"
    url = "https://bitbucket.org/joezuntz/cosmosis/get/v1.6.2.tar.bz2"
    git = "https://bitbucket.org/joezuntz/cosmosis.git"

    # cosmosis by default links some .so files with a full path; so
    # fix that...
    patch("linking_patch")

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version("des-y3", tag="des-y3")
    version("neutrinoless_mass_function_2", commit="a7f39b5af97f863ed9297b2e536548db7f425110")
    version("neutrinoless_mass_function_1", commit="790b718ea6d7f47f6d3f8fb6d7340e69709066ac")
    version("1.6.2", sha256="b4e5edb9c144b8bf404a3af554f526f52494c48e81c47c53d61d172d27b823b1")

    # three resources for the des-y3 tag:
    resource(
        name="cosmosis-standard-library",
        git="https://bitbucket.org/joezuntz/cosmosis-standard-library.git",
        commit="3246f0741551bee1c0d29208e74f38f4ed27d3ed",
        destination=".",
        when="@des-y3",
    )
    resource(
        name="cosmosis-des-library",
        git="https://darkenergysurvey@bitbucket.org/joezuntz/cosmosis-des-library.git",
        tag="des-y3",
        destination=".",
        when="@des-y3",
    )
    resource(
        name="y3-3x2pt",
        git="https://github.com/des-science/y3-3x2pt.git",
        tag="des-y3",
        destination=".",
        when="@des-y3",
    )

    # the rest just have cosmosis-standard-library
    resource(
        name="cosmosis-standard-library",
        git="https://bitbucket.org/joezuntz/cosmosis-standard-library.git",
        commit="30e90c9e8882aa6505e2019ad8b6ef4196471109",
        destination=".",
        when="@neutrinoless_mass_function_2",
    )
    resource(
        name="cosmosis-standard-library",
        git="https://bitbucket.org/joezuntz/cosmosis-standard-library.git",
        commit="1daec6833c0d521ae0f7168f932d5ce6ebed6fa4",
        destination=".",
        when="@neutrinoless_mass_function_1",
    )
    resource(
        name="cosmosis-standard-library",
        git="https://bitbucket.org/joezuntz/cosmosis-standard-library.git",
        tag="v1.6.2",
        destination=".",
        when="@1.6.2",
    )

    depends_on("py-configparser")
    depends_on("py-future")
    depends_on("py-ipython")
    depends_on("py-python-dateutil")
    depends_on("py-tornado")
    # depends_on('py-astropy -usesystemlib')
    depends_on("py-astropy")
    depends_on("py-matplotlib@2.0.0:")
    depends_on("py-mpi4py")
    depends_on("py-emcee")
    depends_on("py-numpy")
    depends_on("py-pyyaml")
    depends_on("py-cython")
    depends_on("py-scipy")
    depends_on("mpich")
    depends_on("openblas")
    depends_on("gsl")
    depends_on("fftw")
    depends_on("minuit")
    depends_on("sqlite")
    depends_on("cfitsio")

    def setup_build_environment(self, env):
        """Set up the build environment for this package."""
        env.set("COSMOSIS_SRC_DIR", self.prefix)
        env.set("LAPACK_LINK", "-lopenblas")
        env.set("GSL_INC", self.spec["gsl"].prefix + "/include")
        env.set("GSL_LIB", self.spec["gsl"].prefix + "/lib")
        env.set("FFTW_INCLUDE_DIR", self.spec["fftw"].prefix + "/include")
        env.set("FFTW_LIBRARY", self.spec["fftw"].prefix + "/lib")
        env.set("MINUIT2_INC", self.spec["minuit"].prefix + "/include")
        env.set("MINUIT2_LIB", self.spec["minuit"].prefix + "/lib")
        env.set("CFITSIO_INC", self.spec["cfitsio"].prefix + "/include")
        env.set("CFITSIO_LIB", self.spec["cfitsio"].prefix + "/lib")

    def build(self, spec, prefix):
        import inspect

        install_tree(".", prefix)
        with working_dir(prefix):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        # it is already there..but we need a lib directory
        with working_dir(prefix):
            os.system("mkdir lib && cd lib && ln -s `find .. -name *.so -print` .")
        pass

    def setup_run_environment(self, env):
        """Set up the run environment for this package."""
        env.prepend_path("PATH", self.prefix + "/bin")
        env.prepend_path("PYTHONPATH", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix + "/cosmosis/datablock")
        env.prepend_path(
            "LD_LIBRARY_PATH",
            self.prefix + "/cosmosis-standard-library/likelihood/planck/plc-1.0/lib",
        )
        env.prepend_path(
            "LD_LIBRARY_PATH",
            self.prefix + "/cosmosis-standard-library/likelihood/planck2015/plc-2.0/lib",
        )
        env.set("COSMOSIS_SRC_DIR", self.prefix)
        env.set("GSL_LIB", self.spec["gsl"].prefix + "/lib")
        env.set("FFTW_LIBRARY", self.spec["fftw"].prefix + "/lib")
