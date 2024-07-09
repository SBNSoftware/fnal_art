# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MuseExternals(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2ewiki.fnal.gov/wiki/Muse"

    version("p042")
    version("p041")
    version("develop")

    maintainers = ["marcmengel", "rclee", "kutschke"]

    with when("@develop"):
        depends_on("artdaq-core-mu2e", type=("build", "run"))
        depends_on("artdaq-core", type=("build", "run"))
        depends_on("art-root-io", type=("build", "run"))
        depends_on("art", type=("build", "run"))
        depends_on("boost", type=("build", "run"))
        depends_on("btrk", type=("build", "run"))
        depends_on("canvas", type=("build", "run"))
        depends_on("cetlib-except", type=("build", "run"))
        depends_on("cetlib", type=("build", "run"))
        depends_on("clhep", type=("build", "run"))
        depends_on("cryptopp", type=("build", "run"))
        depends_on("fftw", type=("build", "run"))
        depends_on("fhicl-cpp", type=("build", "run"))
        depends_on("g4abla", type=("build", "run"))
        depends_on("g4emlow", type=("build", "run"))
        depends_on("g4incl", type=("build", "run"))
        depends_on("g4ndl", type=("build", "run"))
        depends_on("g4particlexs", type=("build", "run"))
        depends_on("g4photonevaporation", type=("build", "run"))
        depends_on("g4pii", type=("build", "run"))
        depends_on("g4radioactivedecay", type=("build", "run"))
        depends_on("g4realsurface", type=("build", "run"))
        depends_on("geant4", type=("build", "run"))
        depends_on("gsl", type=("build", "run"))
        depends_on("hep-concurrency", type=("build", "run"))
        depends_on("kinkal", type=("build", "run"))
        depends_on("messagefacility", type=("build", "run"))
        depends_on("mu2e-pcie-utils", type=("build", "run"))
        depends_on("openblas", type=("build", "run"))
        depends_on("postgresql", type=("build", "run"))
        depends_on("python", type=("build", "run"))
        depends_on("root", type=("build", "run"))
        depends_on("sqlite", type=("build", "run"))
        depends_on("intel-tbb-oneapi", type=("build", "run"))
        depends_on("trace", type=("build", "run"))
        depends_on("vecgeom", type=("build", "run"))
        depends_on("xerces-c", type=("build", "run"))

    with when("@p042"):
        depends_on("artdaq-core-mu2e@1.09.02", type=("build", "run"))
        depends_on("artdaq-core@3.09.13", type=("build", "run"))
        depends_on("art-root-io@1.12.04", type=("build", "run"))
        depends_on("art@3.13.02", type=("build", "run"))
        depends_on("boost@1.82.0", type=("build", "run"))
        depends_on("btrk@1.02.41", type=("build", "run"))
        depends_on("canvas@3.15.02", type=("build", "run"))
        depends_on("cetlib-except@1.09.01", type=("build", "run"))
        depends_on("cetlib@3.17.01", type=("build", "run"))
        depends_on("clhep@2.4.6.4", type=("build", "run"))
        depends_on("cryptopp@08.02.00", type=("build", "run"))
        depends_on("fftw@3.3.10", type=("build", "run"))
        depends_on("fhicl-cpp@4.18.01", type=("build", "run"))
        depends_on("g4abla@3.1", type=("build", "run"))
        depends_on("g4emlow@7.13", type=("build", "run"))
        depends_on("g4incl@1.0", type=("build", "run"))
        depends_on("g4ndl@4.6", type=("build", "run"))
        depends_on("g4particlexs@3.1.1", type=("build", "run"))
        depends_on("g4photonevaporation@5.7", type=("build", "run"))
        depends_on("g4pii@1.3", type=("build", "run"))
        depends_on("g4radioactivedecay@5.6", type=("build", "run"))
        depends_on("g4realsurface@2.2", type=("build", "run"))
        depends_on("geant4@10.7.4", type=("build", "run"))
        depends_on("gsl@2.7", type=("build", "run"))
        depends_on("hep-concurrency@1.09.01", type=("build", "run"))
        depends_on("kinkal@2.03.01", type=("build", "run"))
        depends_on("messagefacility@2.10.02", type=("build", "run"))
        depends_on("mu2e-pcie-utils@2.08.05", type=("build", "run"))
        depends_on("openblas@0.3.23", type=("build", "run"))
        depends_on("postgresql@15.2", type=("build", "run"))
        depends_on("python@3.9.15", type=("build", "run"))
        depends_on("root@6.28.04", type=("build", "run"))
        depends_on("sqlite@3.40.1", type=("build", "run"))
        depends_on("intel-tbb-oneapi@2021.9.0", type=("build", "run"))
        depends_on("trace@v3_17_09", type=("build", "run"))
        depends_on("vecgeom", type=("build", "run"))
        depends_on("xerces-c@3.2.3", type=("build", "run"))

    with when("@p041"):
        depends_on("artdaq-core-mu2e@1.08.08", type=("build", "run"))
        depends_on("artdaq-core@v3_09_09", type=("build", "run"))
        depends_on("art-root-io@1.12.04", type=("build", "run"))
        depends_on("art@3.13.02", type=("build", "run"))
        depends_on("boost@1.82.0", type=("build", "run"))
        depends_on("btrk@1.02.41", type=("build", "run"))
        depends_on("canvas@3.15.02", type=("build", "run"))
        depends_on("cetlib-except@1.09.01", type=("build", "run"))
        depends_on("cetlib@3.17.01", type=("build", "run"))
        depends_on("clhep@2.4.6.4", type=("build", "run"))
        depends_on("cryptopp@08.02.00", type=("build", "run"))
        depends_on("fftw@3.3.10", type=("build", "run"))
        depends_on("fhicl-cpp@4.18.01", type=("build", "run"))
        depends_on("g4abla@3.1", type=("build", "run"))
        depends_on("g4emlow@7.13", type=("build", "run"))
        depends_on("g4incl@1.0", type=("build", "run"))
        depends_on("g4ndl@4.6", type=("build", "run"))
        depends_on("g4particlexs@3.1.1", type=("build", "run"))
        depends_on("g4photonevaporation@5.7", type=("build", "run"))
        depends_on("g4pii@1.3", type=("build", "run"))
        depends_on("g4radioactivedecay@5.6", type=("build", "run"))
        depends_on("g4realsurface@2.2", type=("build", "run"))
        depends_on("geant4@10.7.4", type=("build", "run"))
        depends_on("gsl@2.7", type=("build", "run"))
        depends_on("hep-concurrency@1.09.01", type=("build", "run"))
        depends_on("kinkal@2.03.01", type=("build", "run"))
        depends_on("messagefacility@2.10.02", type=("build", "run"))
        depends_on("mu2e-pcie-utils@2.08.04", type=("build", "run"))
        depends_on("openblas@0.3.23", type=("build", "run"))
        depends_on("postgresql@15.2", type=("build", "run"))
        depends_on("python@3.9.15", type=("build", "run"))
        depends_on("root@6.28.04", type=("build", "run"))
        depends_on("sqlite@3.40.1", type=("build", "run"))
        depends_on("intel-tbb-oneapi@2021.9.0", type=("build", "run"))
        depends_on("trace@v3_17_09", type=("build", "run"))
        depends_on("vecgeom", type=("build", "run"))
        depends_on("xerces-c@3.2.3", type=("build", "run"))
        depends_on("fftw-api ^fftw")

    def setup_run_environment(self, env):

        deplist = [
            "artdaq-core-mu2e",
            "artdaq-core",
            "art-root-io",
            "art",
            "boost",
            "btrk",
            "canvas",
            "cetlib-except",
            "cetlib",
            "clhep",
            "cryptopp",
            "fhicl-cpp",
            "gsl",
            "hep-concurrency",
            "kinkal",
            "messagefacility",
            "mu2e-pcie-utils",
            "openblas",
            "postgresql",
            "python",
            "root",
            "sqlite",
            "tbb",
            "trace",
            "vecgeom",
            "xerces-c",
        ]
        for dep in deplist:
            env.append_path("LD_LIBRARY_PATH", self.spec[dep].prefix.lib)

        env.set("ARTDAQ_CORE_INC", self.spec["artdaq-core"].prefix.include)
        env.set("ARTDAQ_CORE_MU2E_INC", self.spec["artdaq-core-mu2e"].prefix.include)
        env.set("ART_INC", self.spec["art"].prefix.include)
        env.set("ART_ROOT_IO_INC", self.spec["art-root-io"].prefix.include)
        env.set("BOOST_INC", self.spec["boost"].prefix.include)
        env.set("BTRK_INC", self.spec["btrk"].prefix.include)
        env.set("CANVAS_INC", self.spec["canvas"].prefix.include)
        env.set("CETLIB_EXCEPT_INC", self.spec["cetlib-except"].prefix.include)
        env.set("CETLIB_INC", self.spec["cetlib"].prefix.include)
        env.set("CET_PLUGIN_PATH", self.spec["cetlib-except"].prefix.include)
        env.set("CLHEP_INC", self.spec["clhep"].prefix.include)
        #env.set("CRYHOME", self.spec["cry"].prefix)
        #env.set("CRY_LIB", self.spec["cry"].prefix.include)
        env.set("CRYPTOPP_INC", self.spec["cryptopp"].prefix.include)
        env.set("CRYPTOPP_LIB", self.spec["cryptopp"].prefix.include)
        env.set("FHICLCPP_INC", self.spec["fhicl-cpp"].prefix.include)
        env.set("G4INCLDATA", self.spec["g4incl"].prefix.include)
        env.set("G4INCLUDE", self.spec["geant4"].prefix.include)
        env.set("G4LIB", self.spec["geant4"].prefix.include)
        # note: G4xxxDATA are set by the respective packages
        env.set("GEANT4_VERSION", str(self.spec["geant4"].version))
        env.set("GSL_INC", self.spec["gsl"].prefix.include)
        env.set("HEP_CONCURRENCY_INC", self.spec["hep-concurrency"].prefix.include)
        env.set("KINKAL_INC", self.spec["kinkal"].prefix.include)
        env.set("MESSAGEFACILITY_INC", self.spec["messagefacility"].prefix.include)
        env.set("MU2E_PCIE_UTILS_INC", self.spec["mu2e-pcie-utils"].prefix.include)
        env.set("OPENBLAS_INC", self.spec["openblas"].prefix.include)
        env.set("POSTGRESQL_INC", self.spec["postgresql"].prefix.include)
        env.set("PYTHON_INCLUDE", self.spec["python"].prefix.include)
        env.set("PYTHON_LIBDIR", self.spec["python"].libs.directories[0])
        env.set("ROOT_INC", self.spec["root"].prefix.include)
        env.set("SQLITE_INC", self.spec["sqlite"].prefix.include)
        #env.set("SWIG_VERSION", self.spec["swig"].version)
        env.set("TBB_INC", self.spec["intel-tbb-oneapi"].prefix.include)
        env.set("TRACE_INC", self.spec["trace"].prefix.include)
        env.set("VECGEOM_INC", self.spec["vecgeom"].prefix.include)
        env.set("VECGEOM_LIB", self.spec["vecgeom"].prefix.lib)
        env.set("XERCES_C_INC", self.spec["xerces-c"].prefix.include)
