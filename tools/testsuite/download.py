"""
These commands are related to downloading test suite CI artifacts.
"""
# pylint: disable=resource-leakage,broad-except,3rd-party-module-not-gated
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from ptscripts import Context, command_group

import tools.utils
import tools.utils.gh

with tools.utils.REPO_ROOT.joinpath("cicd", "golden-images.json").open() as rfh:
    OS_SLUGS = sorted(json.load(rfh))

log = logging.getLogger(__name__)


# Define the command group
download = command_group(
    name="download",
    help="Test Suite CI Artifacts Related Commands",
    description=__doc__,
    parent="ts",
)


@download.command(
    name="onedir-artifact",
    arguments={
        "run_id": {
            "help": "The workflow run ID from where to download artifacts from",
            "required": True,
        },
        "platform": {
            "help": "The onedir platform artifact to download",
            "choices": ("linux", "darwin", "windows"),
            "required": True,
        },
        "arch": {
            "help": "The onedir artifact architecture",
            "choices": ("x86_64", "aarch64", "amd64", "x86"),
        },
        "repository": {
            "help": "The repository to query, e.g. saltstack/salt",
        },
    },
)
def download_onedir_artifact(
    ctx: Context,
    run_id: int = None,
    platform: str = None,
    arch: str = "x86_64",
    repository: str = "saltstack/salt",
):
    """
    Download CI onedir artifacts.
    """
    if TYPE_CHECKING:
        assert run_id is not None
        assert platform is not None

    exitcode = tools.utils.gh.download_onedir_artifact(
        ctx=ctx, run_id=run_id, platform=platform, arch=arch, repository=repository
    )
    ctx.exit(exitcode)


@download.command(
    name="nox-artifact",
    arguments={
        "run_id": {
            "help": "The workflow run ID from where to download artifacts from",
            "required": True,
        },
        "slug": {
            "help": "The OS slug",
            "required": True,
            "choices": OS_SLUGS,
        },
        "nox_env": {
            "help": "The nox environment name.",
        },
        "repository": {
            "help": "The repository to query, e.g. saltstack/salt",
        },
    },
)
def download_nox_artifact(
    ctx: Context,
    run_id: int = None,
    slug: str = None,
    nox_env: str = "ci-test-onedir",
    repository: str = "saltstack/salt",
):
    """
    Download CI nox artifacts.
    """
    if TYPE_CHECKING:
        assert run_id is not None
        assert slug is not None

    if slug.endswith("arm64"):
        slug = slug.replace("-arm64", "")
        nox_env += "-aarch64"

    exitcode = tools.utils.gh.download_nox_artifact(
        ctx=ctx, run_id=run_id, slug=slug, nox_env=nox_env, repository=repository
    )
    ctx.exit(exitcode)


@download.command(
    name="pkgs-artifact",
    arguments={
        "run_id": {
            "help": "The workflow run ID from where to download artifacts from",
            "required": True,
        },
        "slug": {
            "help": "The OS slug",
            "required": True,
            "choices": OS_SLUGS,
        },
        "repository": {
            "help": "The repository to query, e.g. saltstack/salt",
        },
    },
)
def download_pkgs_artifact(
    ctx: Context,
    run_id: int = None,
    slug: str = None,
    repository: str = "saltstack/salt",
):
    """
    Download CI built packages artifacts.
    """
    if TYPE_CHECKING:
        assert run_id is not None
        assert slug is not None

    exitcode = tools.utils.gh.download_pkgs_artifact(
        ctx=ctx, run_id=run_id, slug=slug, repository=repository
    )
    ctx.exit(exitcode)
