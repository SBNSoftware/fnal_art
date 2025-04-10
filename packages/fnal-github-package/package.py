# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import bisect
import functools
import re
from functools import wraps
from pathlib import Path

import llnl.util.tty as tty

import spack.util.spack_json as sjson
import spack.util.web
from spack.directives import variant
from spack.package import *
from spack.util.environment import PrependPath
from spack.version import *

# Python versions older than 3.9 do not support functools.cache
cache_property = getattr(functools, "cache", functools.lru_cache())

RE_VERSION = re.compile(r"^v")
RE_UPS_STYLE = re.compile(r"^v(\d+)(_\d+)*.*")
RE_DOT_STYLE = re.compile(r"(\d+)(\.\d+)*.*")


def preset_args(source_path, preset):
    if (Path(source_path) / "CMakePresets.json").exists():
        return ["--preset", preset]
    return []


def cmake_preset(f):
    @wraps(f)
    def wrapped_cmake_args(pkg):
        # Should we decide to support 'debug' and 'prof'
        # variants/builds at some point, presumably there will be
        # different CMake presets for those, and those can be
        # specified by interrogating the 'pkg' object.
        return preset_args(pkg.stage.source_path, "default") + f(pkg)

    return wrapped_cmake_args


def sanitize_environment(env, *env_paths):
    for path in env_paths:
        env.prune_duplicate_paths(path)
        env.deprioritize_system_paths(path)


def sanitize_paths(f):
    @wraps(f)
    def wrapped_setup_build_environment(pkg, env, *extra_args):
        f(pkg, env, *extra_args)
        paths = [mod.name for mod in env.env_modifications if type(mod) == PrependPath]
        sanitize_environment(env, *paths)

    return wrapped_setup_build_environment


def dotted_version_str(name):
    linted = RE_VERSION.sub("", name)
    return Version(linted).dotted


def github_version_url(organization, repo_name, native_version_str):
    return f"https://github.com/{organization}/{repo_name}/archive/{native_version_str}.tar.gz"


def fetch_remote_tags(organization, repo_name, url):
    _, _, request = spack.util.web.read_from_url(url, accept_content_type="application/json")
    return {
        dotted_version_str(d["name"]): github_version_url(organization, repo_name, d["name"])
        for d in sjson.load(request)
    }


# wrapped variant to remove boilerplate for "cxxstd"
_disallowed_kwargs = {"multi", "description", "values"}


def cxxstd_variant(*cxxstd_options, **kwargs):
    disallowed_present = set(kwargs.keys()) & _disallowed_kwargs
    if disallowed_present:
        tty.die(
            f"The following keyword arguments cannot be specified to cxxstd_variant: {disallowed_present}"
        )

    variant(
        "cxxstd",
        values=cxxstd_options,
        **kwargs,
        multi=False,
        description="Use the specified C++ standard when building.",
    )


class FnalGithubPackage(Package):
    """Dummy package to provide utilities to real packages.
    This package cannot be installed.
    """

    @property
    def git(self):
        return f"https://github.com/{self.repo}"

    @property
    def homepage(self):
        return self.git

    @property
    def urls(self):
        # We reverse the URLs because Spack specially treats the first one.
        urls_for_tags = [self._url_for_tag(p) for p in self.version_patterns]
        urls_for_tags.reverse()
        return urls_for_tags

    @property
    def list_url(self):
        return f"{self.git}/tags"

    def _url_for_tag(self, version_str):
        return f"{self.git}/archive/refs/tags/{version_str}.tar.gz"

    @property
    @cache_property
    def _version_patterns(self):
        self.version_patterns.sort(key=dotted_version_str)
        result = []
        for p in self.version_patterns:
            version_to_use = dotted_version_str(p)
            if RE_UPS_STYLE.match(p):
                result.append((version_to_use, lambda v: f"v{v.underscored}"))
            elif RE_DOT_STYLE.match(p):
                result.append((version_to_use, lambda v: v))
            else:
                tty.die(f"Version string {p} not supported")
        return result

    def url_for_version(self, version):
        patterns = [p[0] for p in self._version_patterns]
        index = bisect.bisect_right(patterns, version)
        if index != 0:
            index = index - 1
        assert index != len(patterns)
        return self._url_for_tag(self._version_patterns[index][1](version))
