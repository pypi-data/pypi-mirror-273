# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Sequence

from fm_tools.exceptions import ToolInfoNotResolvedError

from .benchexec_helper import load_tool_info

if TYPE_CHECKING:
    from benchexec.tools.template import BaseTool2

    from .fmdata import FmData


@dataclass(frozen=True)
class Limits:
    """
    Dataclass representing the desired limits for the execution of a tool.
    The limits *are not enforced nor guaranteed*. They merely serve as optional
    data that is used while generating the command line for a tool.

    """

    cpu_time: Optional[int] = None
    wall_time: Optional[int] = None
    memory: Optional[int] = None
    cores: Optional[int] = None

    def as_benchexec_limits(self) -> "BaseTool2.ResourceLimits":
        from benchexec.tools.template import BaseTool2

        return BaseTool2.ResourceLimits(
            cputime=self.cpu_time,
            cputime_hard=self.cpu_time,
            walltime=self.wall_time,
            memory=self.memory,
            cpu_cores=self.cores,
        )


def command_line(
    fm_data: "FmData",
    tool_dir: Path,
    input_files: Optional[Sequence[Path]] = None,
    working_dir: Optional[Path] = None,
    property: Optional[Path] = None,  # noqa: A002
    options: Optional[List[str]] = None,
    limits: Optional[Limits] = None,
) -> List[str]:

    from benchexec.tools.template import BaseTool2

    options = options or []

    if not fm_data.get_toolinfo_module():
        raise ToolInfoNotResolvedError(
            "The toolinfo module must be resolved before generating the command line."
        )

    locator = BaseTool2.ToolLocator(tool_directory=tool_dir)
    try:
        _, tool = load_tool_info(str(fm_data.get_toolinfo_module()))
    except (ImportError, ModuleNotFoundError) as e:
        raise ToolInfoNotResolvedError(
            "Could not load toolinfo module. "
            "Make sure it is available in the sys.path, e.g., by calling the make_available() method. "
            f"Original error was: {repr(e)}"
        ) from e

    executable = tool.executable(locator)

    task = BaseTool2.Task.with_files(input_files, property_file=property)
    rlimits = limits.as_benchexec_limits() if limits else BaseTool2.ResourceLimits()

    return tool.cmdline(executable, options, task, rlimits)
