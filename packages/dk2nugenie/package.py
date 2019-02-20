# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Dk2nugenie(Package):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files.
"""
    homepage = "https://cdcvs.fnal.gov/redmine/projects/dk2nu"
    url      = "http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02"

    version('01_07_02',  svn="http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02")

    depends_on('cmake', type='build')
    depends_on('root')
    depends_on('libxml2')
    depends_on('log4cpp')
    depends_on('genie')
    depends_on('dk2nudata')

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    parallel = False

    def set_cxxstdflag(self):
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
        return cxxstdflag

    def patch(self):
        cmakelists=FileFilter('{0}/dk2nu/genie/CMakeLists.txt'.format(self.stage.source_path))
        cmakelists.filter('\$\{GENIE\}/src', '${GENIE}/include/GENIE')

    def install(self, spec, prefix):
        args = ['-DCMAKE_INSTALL_PREFIX=%s'%prefix,
                '-DGENIE_ONLY=ON',
                '-DTBB_LIBRARY=%s/libtbb.so'%self.spec['intel-tbb'].prefix.lib,
                '-DGENIE_INC=%s/GENIE'%self.spec['genie'].prefix.include,
                '-DDK2NUDATA_DIR=%s'%self.spec['dk2nudata'].prefix.lib ,
                '%s/dk2nu' % self.stage.source_path ]
        cmake = which('cmake')
        with working_dir('%s/spack-build'%self.stage.path, create=True):
            cmake(*args)
            make('VERBOSE=t', 'all','install')
