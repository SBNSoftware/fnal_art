# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os,glob

class Genie(Package):
    """GENIE is an international collaboration of scientists that plays the 
leading role in the development of comprehensive physics models for 
the simulation of neutrino interactions, and performs a highly-developed
global analysis of neutrino scattering data. 
"""

    homepage = "http://www.genie-mc.org"
    url      = "https://github.com/GENIE-MC/Generator/archive/R-2_12_10.tar.gz"

    version('3_00_02', sha256='34d6c37017b2387c781aea7bc727a0aac0ef45d6b3f3982cc6f3fc82493f65c3')
    version('3_0_0b4', sha256='41100dd5141a7e2c934faaaf22f244deda08ab7f03745976dfed0f31e751e24e')
    version('3_0_0b3', sha256='96b849d426f261a858f5483f1ef576cc15f5303bc9c217a194de2500fb59cc56')
    version('3_0_0b2', sha256='2884f5cb80467d3a8c11800421c1d1507e9374a4ba2fbd654d474f2676be28ba')
    version('3_0_0b1', sha256='e870146bfa674235c3713a91decf599d2e90b4202f8b277bf49b04089ee432c1')
    version('3_00_00', sha256='3953c7d9f1f832dd32dfbc0b9260be59431206c204aec6ab0aa68c01176f2ae6')
    version('2_12_10', sha256='c8762db3dcc490f80f8a61268f5b964d4d35b80134b622e89fe2307a836f2a0b',preferred=True)
    version('2_12_8',  sha256='7ca169a8d9eda7267d28b76b2f3110552852f8eeae263a03cd5139caacebb4ea')
    version('2_12_6',  sha256='3b450c609875459798ec98e12cf671cc971cbb13345af6d75bd6278d422f3309')
    version('2_12_4',  sha256='19a4a1633b0847a9f16a44e0c74b9c224ca3bb93975aecf108603c22e807517b')

    depends_on('root')
    depends_on('lhapdf')
    depends_on('pythia6')
    depends_on('libxml2')
    depends_on('log4cpp')

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    def setup_environment(self, spack_env, run_env):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag = ''
        if cxxstd == '98':
            cxxstdflag = self.compiler.cxx98_flag
        elif cxxstd == '11':
            cxxstdflag = self.compiler.cxx11_flag
        elif cxxstd == '14':
            cxxstdflag = self.compiler.cxx14_flag
        elif cxxstd == '17':
            cxxstdflag = self.compiler.cxx17_flag
        elif cxxstd == 'default':
            pass
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die(
                "INTERNAL ERROR: cannot accommodate unexpected variant ",
                "cxxstd={0}".format(spec.variants['cxxstd'].value))

        spack_env.append_flags('CXXFLAGS', cxxstdflag)

 
    def install(self, spec, prefix):
        args = [
                '--enable-lhapdf',
                '--enable-rwght',
                '--enable-fnal',
                '--enable-atmo',
                '--enable-event-server',
                '--enable-nucleon-decay',
                '--enable-neutron-osc',
                '--enable-vle-extension',
                '--with-pythia6-lib={0}/libpythia.so'.format(self.spec['pythia6'].prefix.lib),
                '--with-lhapdf-lib={0}'.format(self.spec['lhapdf'].prefix.lib),
                '--with-lhapdf-inc={0}'.format(self.spec['lhapdf'].prefix.inc),
                '--with-libxml2-inc={0}'.format(self.spec['libxml2'].prefix.inc),
                '--with-libxml2-lib={0}'.format(self.spec['libxml2'].prefix.lib),
                '--with-log4cpp-inc={0}'.format(self.spec['log4cpp'].prefix.inc),
                '--with-log4cpp-lib={0}'.format(self.spec['log4cpp'].prefix)
                ]
        with working_dir(join_path(self.stage.path,'spack-build'), create=True):
            configure=which(join_path(self.stage.source_path,'configure'))
            configure(*args)          
            make('GOPT_WITH_CXX_USERDEF_FLAGS="{0}"'.format(os.env('CXXFLAGS')))
            make('check')
            make('install')
