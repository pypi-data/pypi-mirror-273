import logging
import os
from pathlib import Path

import dotenv

from atlas_init.cli_helper.run import run_command_is_ok
from atlas_init.settings.config import TestSuite
from atlas_init.settings.env_vars import AtlasInitSettings

logger = logging.getLogger(__name__)


def run_go_tests(
    repo_path: Path,
    repo_alias: str,
    package_prefix: str,
    settings: AtlasInitSettings,
    groups: list[TestSuite],
):
    test_env = os.environ | dotenv.dotenv_values(settings.env_vars_vs_code)
    for group in groups:
        packages = ",".join(f"{package_prefix}/{pkg}" for pkg in group.repo_go_packages.get(repo_alias, []))
        if not packages:
            logger.warning(f"no go packages for suite: {group}")
            continue
        command = f"go test {packages} -v -run ^TestAcc* -timeout 300m".split(" ")
        if not group.sequential_tests:
            command.extend(["-parallel", "20"])
        is_ok = run_command_is_ok(command, test_env, cwd=repo_path, logger=logger)
        assert is_ok, f"go tests failed for {group}"
