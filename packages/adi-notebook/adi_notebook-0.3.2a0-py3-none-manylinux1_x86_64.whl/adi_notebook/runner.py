from __future__ import annotations

import contextlib
import datetime
import inspect
import json
import multiprocessing
import os
import pathlib
import pickle
import sys

# from contextlib import redirect_stderr
from copy import deepcopy
from dataclasses import dataclass, field, fields
from functools import cached_property
from io import StringIO
from typing import Any, Callable, Generic, TypeVar, overload

import dsproc3 as dsproc
import pandas as pd
import requests  # type: ignore
import tqdm

# from wurlitzer import pipes  # type: ignore
import wurlitzer
import xarray as xr
from adi_py import ADILogger, Process, SkipProcessingIntervalException  # type: ignore
from adi_py.utils import is_empty_function  # type: ignore
from mock import patch  # type: ignore
from tqdm import tqdm

from .constant import CONSTANT

VapProcess = TypeVar("VapProcess", bound=Process)
ProcessHookManager = TypeVar("ProcessHookManager")
USER_HOME = f'/home/{os.environ["USER"]}'
DATA_HOME = f'/data/home/{os.environ["USER"]}/data'  # Note: convention for ARM server


ADI_ENV_VAR_DEFAULT = {
    "DATASTREAM_DATA_IN": "/data/archive",
    "DATASTREAM_DATA_OUT": f"{DATA_HOME}/datastream",
    "QUICKLOOK_DATA": f"{DATA_HOME}/quicklook",
    "LOGS_DATA": f"{DATA_HOME}/logs",
    "CONF_DATA": f"{DATA_HOME}/conf",
    "ADI_PY_MODE": "development",
    "ADI_CACHE_DIR": f"{USER_HOME}/.adi_tmp",
}


class Util:
    @staticmethod
    def validate_input_path(path: str):
        if not os.access(path, os.R_OK):
            raise ValueError(
                f"Invalid env_var {path}. Path does not exist or have Read Permissions."
            )
        return True

    @staticmethod
    def validate_output_path(path: str):
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                assert os.access(path, os.W_OK)
            except Exception as e:
                print(e)
                raise ValueError(
                    f"Invalid env_var {path}. Path does not have Write Permissions."
                )
        return True

    @staticmethod
    def to_datetime(date: str, format: str = "%Y%m%d") -> datetime.datetime:
        try:
            assert len(date) == 8
            return datetime.datetime.strptime(date, format)
        except ValueError or AssertionError:
            raise ValueError(
                f'Invalid date={date}. Needs to be a valid date in the "%Y%m%d" format.(e.g., 20200101.).'
            )

    @staticmethod
    def validate_begin_end_dates(begin_date, end_date):
        if not Util.to_datetime(begin_date) and (
            Util.to_datetime(begin_date) < datetime.datetime(1992, 1, 1)
        ):
            raise ValueError(
                f"begin_date={begin_date} is less than the earliest ARM data=19920101."
            )
        if not Util.to_datetime(end_date) and (
            Util.to_datetime(end_date) <= Util.to_datetime(begin_date)
        ):
            raise ValueError(
                f"end_date={end_date} needs to be greater than the begin_date={begin_date}."
            )

    @staticmethod
    def get_proc_log_file_paths(process_name: str, site: str, facility: str):
        """
        EXAMPLE:
        Util.get_proc_log_file_paths("adi_demo_5_multi_in_coord_out","sgp", "C1")
        >>
        ['/data/home/.../data/logs/sgp/proc_logs/sgpadi_demo_5_multi_in_coord_outC1/sgpadi_demo_5_multi_in_coord_outC1.20240400.000000.VAP',
        '/data/home/.../data/logs/sgp/proc_logs/sgpadi_demo_5_multi_in_coord_outC1/sgpadi_demo_5_multi_in_coord_outC1.20240500.000000.VAP',
        '/data/home/.../data/logs/sgp/proc_logs/sgpadi_demo_5_multi_in_coord_outC1/sgpadi_demo_5_multi_in_coord_outC1.20240500.000000.VAP']
        """
        parent_path: str = f'{ADI_ENV_VAR_DEFAULT["LOGS_DATA"]}/{site}/proc_logs/{site}{process_name}{facility}'
        files = os.listdir(parent_path)
        abs_files: list[str] = [
            os.path.abspath(os.path.join(parent_path, f)) for f in files
        ]
        abs_files.sort(key=os.path.getctime, reverse=True)  # sorted from new to old
        return abs_files

    @staticmethod
    def get_newest_proc_log_file_path(process_name: str, site: str, facility: str):
        """
        EXAMPLE:
        Util.get_proc_log_file_paths("adi_demo_5_multi_in_coord_out","sgp", "C1")
        >>
        '/data/home/.../data/logs/sgp/proc_logs/sgpadi_demo_5_multi_in_coord_outC1/sgpadi_demo_5_multi_in_coord_outC1.20240400.000000.VAP'
        """
        abs_files = Util.get_proc_log_file_paths(process_name, site, facility)
        abs_files.sort(key=os.path.getctime, reverse=True)  # sorted from new to old
        return abs_files[0]

    @staticmethod
    def fetch_last_n_lines(
        file_path: str,
        n_last_lines: int = -1,
        stop_word: str | None = None,
        pattern_times: tuple[str, int] | None = None,
    ) -> list[str]:
        """
        Fetch last several lines of a file based on three modes:
        1, n_last_lines > 0, fetch last n_last_lines lines
        2. if stop_word is not None, fetch the last chunk of files including the stop word
        3. if pattern_times is not None, fetch the last chunk of files including the pattern that repeat n times.
        Note: for performance concern, not fetch the whole file.
        Note: using batch search, the header might not include the stop word or pattern.
        EXAMPLE:
        >>
        ['Resident Set Size:     198948 Kbytes\n',
        'Total CPU Time:        40.05 seconds\n',
        '\n',
        'Run time: 1 seconds\n',
        '**** CLOSED: 2024-04-23 19:28:31\n']"""
        # ref: https://www.geeksforgeeks.org/python-reading-last-n-lines-of-a-file/
        with open(file_path) as f:
            buffer_size = 128
            f_size = os.stat(file_path).st_size
            if buffer_size > f_size:
                buffer_size = f_size - 1  # adjusting buffer size
            iter = 0
            pointer = f.seek(0, 2)  # to the end of the file
            fetched_lines = []
            while pointer > 0:
                iter += 1
                pointer = pointer - iter * buffer_size  # moving pointer backward
                if pointer < 0:
                    pointer = 0
                f.seek(pointer)
                fetched_lines = f.readlines()
                if n_last_lines > 0 and len(fetched_lines) >= n_last_lines:
                    break
                if stop_word and stop_word in "".join(fetched_lines):
                    break
                if (
                    pattern_times
                    and len(
                        [line for line in fetched_lines if pattern_times[0] in line]
                    )
                    >= pattern_times[1]
                ):
                    break
            return fetched_lines

    @staticmethod
    def get_last_proc_log_from_file(
        file_path: str, start_pattern: str = "**** OPEN"
    ) -> str:
        """
        EXAMPLE:
        get_last_proc_log_from_file(file_path)
        >>
        ['**** OPENED: 2024-04-23 01:22:05\n',
        '\n',
        'Processing data: 2018-11-03 00:00:00 -> 2018-11-04 00:00:00\n',
        'Using interpolation for dim range in field ceil_backscatter\n',
        'Using bin averaging for dim time in field ceil_first_cbh\n',
        ...
        'Run time: 3 seconds\n',
        '**** CLOSED: 2024-04-23 01:22:08\n']
        """

        raw_log_lines = Util.fetch_last_n_lines(file_path, stop_word=start_pattern)
        last_log = []
        for line in raw_log_lines[::-1]:
            last_log.append(line)
            if start_pattern in line:
                break
        return "".join(last_log[::-1])

    @staticmethod
    def get_proc_logs_since(): ...  # TODO: get logs since certain datetime

    @staticmethod
    def get_last_n_proc_log_from_file(
        file_path: str, start_pattern: str = "**** OPEN", n_appearance: int = -1
    ) -> str:
        """
        EXAMPLE:
        get_last_n_proc_log_from_file(file_path)
        >>
        ['**** OPENED: 2024-04-23 01:22:05\n',
        '\n',
        'Processing data: 2018-11-03 00:00:00 -> 2018-11-04 00:00:00\n',
        'Using interpolation for dim range in field ceil_backscatter\n',
        'Using bin averaging for dim time in field ceil_first_cbh\n',
        ...
        'Run time: 3 seconds\n',
        '**** CLOSED: 2024-04-23 01:22:08\n']
        """

        raw_log_lines = Util.fetch_last_n_lines(
            file_path, pattern_times=(start_pattern, n_appearance)
        )
        last_n_logs = []
        if n_appearance > 0:
            n_found = 0
        else:
            n_found = n_appearance
        for line in raw_log_lines[::-1]:
            last_n_logs.append(line)
            if n_appearance > 0 and start_pattern in line:
                n_found += 1
            if n_found == n_appearance:
                break
        assert (
            len([line for line in last_n_logs if start_pattern in line]) == n_appearance
        ), f"{start_pattern=} didn't appear {n_appearance=} times in the file."
        return "".join(last_n_logs[::-1])


@dataclass
class AdiRunner:
    process_name: str

    # TODO: Allow extra args for flexibility and backward compatible. But how to do that for dataclass

    # TODO: adding limitation how many intervals can be loaded into memory to prevent crashing.
    # TODO: adding option not to dump intermediate file on local path (i.e., as part of the caching mechanism)
    # TODO: adding option not to dump input datasets for caching
    # TODO: adding option not to dump transformed datasets for caching

    site: str
    facility: str
    begin_date: str
    end_date: str

    pcm_link: str | None = field(default=None, init=False, repr=True)

    DATASTREAM_DATA_IN: str = field(
        default_factory=lambda: os.getenv("DATASTREAM_DATA_IN", ""),
        repr=True,
    )
    DATASTREAM_DATA_OUT: str = field(
        default_factory=lambda: os.getenv("DATASTREAM_DATA_OUT", ""),
        repr=True,
    )
    QUICKLOOK_DATA: str = field(
        default_factory=lambda: os.getenv("QUICKLOOK_DATA", ""),
        repr=True,
    )
    LOGS_DATA: str = field(
        default_factory=lambda: os.getenv("LOGS_DATA", ""),
        repr=True,
    )
    CONF_DATA: str = field(
        default_factory=lambda: os.getenv("CONF_DATA", ""),
        repr=True,
    )
    ADI_PY_MODE: str = field(
        default_factory=lambda: os.getenv("ADI_PY_MODE", ""),
        repr=True,
    )

    ADI_CACHE_DIR: str = field(
        default_factory=lambda: os.getenv("ADI_CACHE_DIR", ""),
        repr=True,
    )

    process_class_type: type[Process] = field(
        default=Process, repr=False
    )  # should be type[VapProcess]

    # TODO: Create Protocol/more accurate type hints for each hook function
    init_process_hook: Callable = field(
        default=Process.init_process_hook, repr=False, kw_only=True
    )
    pre_retrieval_hook: Callable = field(
        default=Process.pre_retrieval_hook, repr=False, kw_only=True
    )
    post_retrieval_hook: Callable = field(
        default=Process.post_retrieval_hook, repr=False, kw_only=True
    )
    pre_transform_hook: Callable = field(
        default=Process.pre_transform_hook, repr=False, kw_only=True
    )
    post_transform_hook: Callable = field(
        default=Process.post_transform_hook, repr=False, kw_only=True
    )
    process_data_hook: Callable = field(
        default=Process.process_data_hook, repr=False, kw_only=True
    )
    finish_process_hook: Callable = field(
        default=Process.finish_process_hook, repr=False, kw_only=True
    )
    quicklook_hook: Callable = field(
        default=Process.quicklook_hook, repr=False, kw_only=True
    )

    def __post_init__(self):
        self.pcm = PCM(self.process_name)
        self.sys_argv = SysArgv(
            self.process_name, self.site, self.facility, self.begin_date, self.end_date
        )
        self.controller = None
        self.process_hook_manager: ProcessHookManager = setup_process_hook(self)  # type: ignore

        self.process_env_var_manager = setup_environment_variables(self)
        print("self.process_env_var_manager = setup_environment_variables(self)")
        print(os.environ.get("ADI_CACHE_DIR"))

    @property
    def retrieval_rule_sets(self):
        return self.pcm.retrieval_rule_sets

    @property
    def mappings(self):
        return self.pcm.mappings

    @property
    def output_datastreams(self):
        return self.pcm.output_datastreams

    def run_data_consolidator(
        self,
        debug_level: int = 2,
        show_progressbar: bool = True,
        smart_cache: bool = True,
        *args,
        **kwargs,
    ) -> ProcessStatus:
        self.controller = RunnerController(
            sys_argv=self.sys_argv,
            process_hook_manager=self.process_hook_manager,  # type: ignore
            process_env_var_manager=self.process_env_var_manager,  # type: ignore
            # process_cache=self.process_cache,
            # self.pcm,
        )
        return self.controller.run(
            run_type="dc",
            debug_level=debug_level,
            show_progressbar=show_progressbar,
            smart_cache=smart_cache,
        )

    def run_vap(
        self,
        debug_level: int = 2,
        show_progressbar: bool = True,
        smart_cache: bool = True,
        *args,
        **kwargs,
    ) -> ProcessStatus:
        self.controller = RunnerController(
            sys_argv=self.sys_argv,
            process_hook_manager=self.process_hook_manager,  # type: ignore
            process_env_var_manager=self.process_env_var_manager,  # type: ignore
            # process_cache=self.process_cache,
            # self.pcm,
        )
        return self.controller.run(
            run_type="vap",
            debug_level=debug_level,
            show_progressbar=show_progressbar,
            smart_cache=smart_cache,
        )

    @property
    def input_datasets(self) -> DataShelf:
        input_datasets = (
            self.controller.process_wrapper.input_datasets
            if self.controller is not None
            else DataShelf()
        )
        if not input_datasets._data:
            self._empty_datastore_warning()
        return input_datasets

    @property
    def transformed_datasets(self) -> DataShelf:
        transformed_datasets = (
            self.controller.process_wrapper.transformed_datasets
            if self.controller is not None
            else DataShelf()
        )
        if not transformed_datasets._data:
            self._empty_datastore_warning()
        return transformed_datasets

    @property
    def output_placeholder_datasets(self) -> DataShelf:
        output_placeholder_datasets = (
            self.controller.process_wrapper.output_placeholder_datasets
            if self.controller is not None
            else DataShelf()
        )
        if not output_placeholder_datasets._data:
            self._empty_datastore_warning()
        return output_placeholder_datasets

    @property
    def output_datasets(self) -> DataShelf:
        output_datasets = (
            self.controller.process_wrapper.output_datasets
            if self.controller is not None
            else DataShelf()
        )
        if not output_datasets._data:
            self._empty_datastore_warning()
        return output_datasets

    def _empty_datastore_warning(self):
        print("Warning: no data has been processed, process data first.")

    def create_process_mock(self) -> ProcessMock:
        if not self.controller:
            print(
                f"Warning: the returned {ProcessMock().__class__.__name__} object will be empty."
            )
        process_mock: ProcessMock = ProcessMock(
            input_datasets=self.input_datasets,
            transformed_datasets=self.transformed_datasets,
            output_placeholder_datasets=self.output_placeholder_datasets,
        )
        return process_mock


def setup_environment_variables(adi_runner: AdiRunner):
    @dataclass
    class ProcessEnvVarManager:
        DATASTREAM_DATA_IN: str
        DATASTREAM_DATA_OUT: str
        QUICKLOOK_DATA: str
        LOGS_DATA: str
        CONF_DATA: str
        ADI_PY_MODE: str
        ADI_CACHE_DIR: str

        def __init__(self):
            self._setup_environment_variables()

        def _setup_environment_variables(self):
            """Helper function to setup env var,
            Precedence: 1. Valid API inputs,
                        2. Existing OS environment variables,
                        3. Reasonable Default.
            Then update the instance fields accordingly"""

            for name, value in ADI_ENV_VAR_DEFAULT.items():
                # Note: getattr(adi_runner, name, None) can return "", for example:
                # DATASTREAM_DATA_IN: str | None = field(default_factory=lambda: os.getenv("DATASTREAM_DATA_IN"))
                # Existing env_vars has higher priority.
                existing_runner_value = getattr(adi_runner, name, None)
                if existing_runner_value:
                    value = existing_runner_value
                ProcessEnvVarManager._validate_environment_variable(
                    name=name, value=value
                )
                os.environ[name] = value
                setattr(adi_runner, name, value)  # update fields
                setattr(self, name, value)  # update fields

        @staticmethod
        def _validate_environment_variable(name: str, value: str):
            if name == "ADI_PY_MODE":
                adi_py_modes = ["development", "production"]
                if value not in adi_py_modes:
                    raise ValueError(
                        f"Invalid env_var {name}={value}. Not in {adi_py_modes}."
                    )
            elif name == "DATASTREAM_DATA_IN":
                try:
                    Util.validate_input_path(value)
                except ValueError:
                    raise ValueError(
                        f"Invalid env_var {name}={value}. Path does not exist or have Read Permissions."
                    )
            else:
                try:
                    Util.validate_output_path(value)
                except ValueError:
                    raise ValueError(
                        f"Invalid env_var {name}={value}. Path does not have Write Permissions."
                    )

    return ProcessEnvVarManager()


@dataclass
class SysArgv:
    # TODO: The concept of SysArgv might be obsolete, site, facility should be part of the runner controller, similar to date
    process_name: str

    site: str
    facility: str
    begin_date: str
    end_date: str

    def __post_init__(self):
        # self.pcm = PCM(self.process_name)
        PCM.validate_pcm_site_facility(self.process_name, self.site, self.facility)
        Util.validate_begin_end_dates(self.begin_date, self.end_date)

    # def validate_pcm_site_facility(self):
    #     if (self.site, self.facility) not in self.pcm.site_facilities:
    #         raise ValueError(
    #             f"(site, facility): ({self.site}, {self.facility})"
    #             f"is not in the defined pcm site_facilities {self.pcm.site_facilities}. (case-sensitive.)"
    #         )

    # def validate_date(self):
    #     if not Util.to_datetime(self.begin_date) and (
    #         Util.to_datetime(self.begin_date) < datetime.datetime(1992, 1, 1)
    #     ):
    #         raise ValueError(
    #             f"begin_date={self.begin_date} is less than the earliest ARM data=19920101."
    #         )
    #     if not Util.to_datetime(self.end_date) and (
    #         Util.to_datetime(self.end_date) <= Util.to_datetime(self.begin_date)
    #     ):
    #         raise ValueError(
    #             f"end_date={self.end_date} needs to be greater than the begin_date={self.begin_date}."
    #         )


# @dataclass
class RunnerController:
    def __init__(
        self,
        sys_argv: SysArgv,
        process_hook_manager,  # type: setup_process_hook.ProcessHookManager
        process_env_var_manager,  # type: setup_environment_variables.ProcessEnvVarManager
    ):
        self.sys_argv = sys_argv
        self.process_hook_manager = process_hook_manager
        self.process_env_var_manager = process_env_var_manager

        self.pcm = PCM(self.sys_argv.process_name)
        self.process_status = ProcessStatus(logs="", terminal_message="")

    def _init_run_(
        self,
        run_type: str,
        debug_level: int = 2,
        show_progressbar: bool = True,
        # show_logs: bool = False,
        smart_cache: bool = True,
        # redirect_stdout: bool = True,
    ):
        assert run_type in [
            "data_consolidate",
            "dc",
            "vap",
            "ingest",
            "ig",
        ], 'run_type not in ["data_consolidate", "dc", "vap", "ingest", "ig"].'
        assert debug_level in [0, 1, 2], "debug_level not in [0, 1, 2]."

        self.run_type: str = run_type
        self.debug_level: int = debug_level
        self.show_progressbar: bool = show_progressbar
        self.smart_cache: bool = smart_cache

        self.process_wrapper = ProcessWrapper(
            # process_name=self.sys_argv.process_name,
            sys_argv=self.sys_argv,
            process_hook_manager=self.process_hook_manager,
            # pcm=self.pcm,
            # process_cache=self.process_cache,
            smart_cache=self.smart_cache,
            data_consolidate_mode=(self.run_type in ["data_consolidate", "dc"]),
        )

    def run(
        self,
        run_type: str,
        debug_level: int = 2,
        show_progressbar: bool = True,
        smart_cache: bool = True,
    ) -> ProcessStatus:
        self._init_run_(
            run_type=run_type,
            debug_level=debug_level,
            show_progressbar=show_progressbar,
            smart_cache=smart_cache,
        )
        return self._run()

    @staticmethod
    def _structure_interval_dates(begin_date, end_date) -> list[tuple[str, str]]:
        """
        EXAMPLE:
        _per_day_interval_list("20100101", ""20100104")
        >> [(20100101, 20100102), (20100102, 20100103), (20100103, 20100104)]"""
        date_list = pd.date_range(
            Util.to_datetime(begin_date),
            Util.to_datetime(end_date),
            freq="D",
        )
        date_list_bound = [
            (dt, dt + pd.DateOffset()) for dt in date_list[:-1]
        ]  # drop end_date
        return [
            (dt1.strftime("%Y%m%d"), dt2.strftime("%Y%m%d"))
            for (dt1, dt2) in date_list_bound
        ]

    def _run_per_processing_interval(
        self, interval_dates: list[tuple[str, str]]
    ) -> None:
        # logs: str = ""
        if self.show_progressbar:
            method_name = type(self.process_status).print_logs.__name__
            print(
                f"Info: show_progressbar = {self.show_progressbar}. \n"
                f"\tYou can view logs later with the `{method_name}` method "
                f"of the returned `{self.process_status.__class__.__name__}` object.\n"
                f"\te.g., status.{method_name}().\n"
            )
        pbar = tqdm(
            interval_dates,
            disable=not self.show_progressbar,
            bar_format="{l_bar}{bar:10} | {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_inv_fmt}]",
        )
        # tqdm bar format: https://github.com/tqdm/tqdm/issues/1259
        # tqdm bar format: https://stackoverflow.com/questions/54362541/how-to-change-tqdms-bar-size
        for interval_begin_date, interval_end_date in pbar:
            pbar.set_description(
                f"Processing {interval_begin_date} --> {interval_end_date}"
            )
            # TODO: discuss how necessary it is to use a patch for the sys.args. (We need to install extra lib mock)
            # Special concern is when there is multiprocessing jobs, the sys.argv can be conflicting.
            # args = [
            sys.argv = self._structure_sys_argv(interval_begin_date, interval_end_date)
            # TODO: using wurlitzer to redirect the terminal message, however this approach not always guarantee updating on the fly.
            # Note: jupyter use web portal to redirect the terminal message, however it might encounter process hanging if the pipe is full.
            with wurlitzer.pipes() as (out, err):
                self.process_wrapper.run()
            message = str(out.getvalue())
            self.process_status.inject(terminal_message=message)
            if not self.show_progressbar:
                print(message)

    def _run(self) -> ProcessStatus:
        sys.argv = self._structure_sys_argv(
            self.sys_argv.begin_date, self.sys_argv.end_date
        )
        if self.can_run_daily:
            # when per_processing_interval == 86400, break down begin - end into per day
            interval_dates = self._structure_interval_dates(
                self.sys_argv.begin_date, self.sys_argv.end_date
            )
            self._run_per_processing_interval(interval_dates)
        else:
            interval_dates = [(self.sys_argv.begin_date, self.sys_argv.end_date)]
            self._run_per_processing_interval(interval_dates)
        # Get logs from LOGS_DATA
        f_path = Util.get_newest_proc_log_file_path(
            self.sys_argv.process_name, self.sys_argv.site, self.sys_argv.facility
        )
        logs = Util.get_last_n_proc_log_from_file(
            f_path, n_appearance=len(interval_dates)
        )
        if self.run_type == "dc":
            logs = ProcessStatus.patch_logs(
                logs, message="Data Consolidate Mode: Successful."
            )
        self.process_status.inject(logs=logs)
        return self.process_status

    @property
    def can_run_daily(self):
        # Note: experiment with run jobs if output_interval == processing_interval == 86400
        intervals: list = [v["interval"] for k, v in self.pcm.output_intervals.items()]
        timezones: list = [v["timezone"] for k, v in self.pcm.output_intervals.items()]
        # TODO: confirm that we don't actually need to check intervals and timezones/offsets
        return (
            self.pcm.processing_interval == 86400
            and [e is None for e in intervals]
            and [e is None for e in timezones]
        )

    def _structure_sys_argv(self, begin_date, end_date):
        proc_args = (
            ["-n", self.sys_argv.process_name]
            # if len(self.wrapped_adi_process.process_names) > 1
            # if len(self.wrapped_adi_process_outer.process_names) > 1
            # else []
        )
        return [
            os.path.realpath(__file__),  # not actually needed
            *proc_args,
            "-s",
            self.sys_argv.site,
            "-f",
            self.sys_argv.facility,
            "-b",
            begin_date,
            "-e",
            end_date,
            "-D",
            f"{self.debug_level}",
            "-R",
            "--dynamic-dods",
        ]


@dataclass
class PCM:  # TODO: implement singleton/cached pool
    """Tracks some information of a PCM Process Definition."""

    process_name: str
    pcm_link: str | None = field(default=None, init=False, repr=True)
    _process_info: dict | None = field(default=None, init=True, repr=False)
    _revision_number: int | None = field(default=None, init=True, repr=False)

    def __post_init__(self):
        self.pcm_link = f"https://pcm.arm.gov/pcm/process/{self.process_name}"
        self._validate_pcm_name()

    def _validate_pcm_name(self):
        if self.process_name not in PCM._existing_processes():
            raise ValueError(
                f'PCM process: "{self.process_name}" is not in the records.'
            )

    def _verify_pcm_api_schema(self): ...  # TODO: verify pcm api schema

    @staticmethod
    def validate_pcm_site_facility(process_name: str, site: str, facility: str):
        pcm = PCM(process_name)
        if (site, facility) not in pcm.site_facilities:
            raise ValueError(
                f"(site, facility): ({site}, {facility})"
                f"is not in the defined pcm site_facilities {pcm.site_facilities}. (case-sensitive.)"
            )

    @property
    def process_info(self) -> dict:
        if self._process_info:
            return self._process_info
        else:
            return self.get_update_process_info()

    def get_update_process_info(self) -> dict:
        url = f"https://pcm.arm.gov/pcm/api/processes/{self.process_name}"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Could not connect to PCM Process API {url}")
            raise ConnectionError(f"Could not connect to PCM Process API '{url}'")
        try:
            self._process_info = res.json()["process"]
            return self._process_info
        except:
            print(
                "An error occurred while attempting to interpret the process definition for"
                f" {self.process_name}. Please ensure the process name is valid."
            )
            raise

    @property
    def revision_number(self):
        if self._revision_number:
            return self._revision_number
        url = f"https://pcm.arm.gov/pcm/api/processes/{self.process_name}/revisions"
        res = requests.get(url)

        if res.status_code != 200:
            print(f"Could not connect to PCM Process API {url}")
            raise ConnectionError(f"Could not connect to PCM Process API '{url}'")
        try:
            self._revision_number = res.json()[-1]["rev_num"]
            return self._revision_number
        except:
            print(
                "An error occurred while attempting to interpret the process definition for"
                f" {self.process_name}. Please ensure the process name is valid."
            )
            raise

    @property
    def existing_processes(self):
        return self._existing_processes()

    @staticmethod
    def _existing_processes() -> list[str]:
        url = "https://pcm.arm.gov/pcm/api/processes"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Could not connect to PCM Process API {url}")
            raise ConnectionError(f"Could not connect to PCM Process API '{url}'")
        return list(res.json().keys())

    @property
    def retrieval_rule_sets(self) -> list[str]:
        process_info = self.process_info
        return list(process_info["variable_retrieval"]["input_datasets"].keys())

    @property
    def input_datastreams(self) -> list[str]:
        process_info = self.process_info
        return process_info["input_datastreams"]

    @property
    def output_datastreams(self) -> list[str]:
        process_info = self.process_info
        return process_info["output_datastreams"]

    @property
    def coordinate_systems(self) -> list[str]:
        process_info = self.process_info
        return list(process_info["variable_retrieval"]["coordinate_systems"].keys())

    @staticmethod
    def construct_mapping(retrieval_rule: str, coordinate: str) -> str:
        return f"{retrieval_rule}+=>{coordinate}"

    @property
    def mappings(self) -> list[str]:
        return [
            self.construct_mapping(retrieval, coord)
            for retrieval, coord in self.mapping_priorities.keys()
            if retrieval and coord
        ]

    @property
    def site_facilities(self) -> list[tuple[str, str]]:
        # Note: case sensitive: site: lowercase, facility: uppercase
        return [
            (location["site"].lower(), location["fac"].upper())
            for location in self._run_locations
        ]

    @property
    def processing_interval(self) -> int:
        processing_interval = int(self.process_info["processing_interval"])
        if processing_interval != 86400:
            print(
                f"Warning: {processing_interval =} != 86400. This is not recommended."
            )
        return processing_interval

    @property
    def output_intervals(self) -> dict[str, dict[str, str | int | None]]:
        """
        EXA<PLE:
        {'adimappedgrid.c1': {'interval': None, 'timezone': None},
        'adiregulargrid.c1': {'interval': None, 'timezone': None},
        'nocoord.c1': {'interval': None, 'timezone': None},
        'nocoord2.c1': {'interval': None, 'timezone': None},
        'testing.c0': {'interval': None, 'timezone': None}}"""
        return self.process_info["output_interval"]

    @property
    def _run_locations(self) -> list[dict[str, str]]:
        process_info = self.process_info
        return process_info["run_locations"]

    # @property
    # def overview(self) -> pd.DataFrame:
    #     return self.get_pcm_plans()

    @property
    def retrieval_rule_set_priorities(self) -> dict[str, dict[int, str]]:
        """
        EXAMPLE:
        {'ceil_b1': {1: 'ceil.b1'},
        'met_b1': {1: 'met.b1', 2: 'met.b1'},
        'twrmr_c1': {1: '1twrmr.c1', 2: 'sirs.b1'}}"""
        df_rules = self._get_filtered_retrieval_rule_set_rules()
        priorities = {}
        for input_dataset, rule in zip(
            df_rules["retrieval_rule_set"].values,
            df_rules.rules.values,
        ):
            priorities[input_dataset] = {
                x["priority"]: x["datastream_name"] for x in rule
            }
        return priorities

    @property
    def mapping_priorities(self) -> dict[tuple[str, str], dict[int, str]]:
        """
        EXAMPLE:
        {('ceil_b1', 'half_min_grid'): {1: 'ceil.b1'},
        ('ceil_b1', 'mapped'): {1: 'ceil.b1'},
        ('met_b1', 'half_min_grid'): {1: 'met.b1', 2: 'met.b1'},
        ('met_b1', None): {1: 'met.b1', 2: 'met.b1'},
        ('twrmr_c1', 'mapped'): {1: '1twrmr.c1', 2: 'sirs.b1'}}"""
        df_rules = self._get_mapping_rules()
        priorities = {}
        for input_dataset, coordinate_system, rule in zip(
            df_rules["retrieval_rule_set"].values,  # TODO: need schema verification
            df_rules.coordinate_system.values,
            df_rules.rules.values,
        ):
            priorities[(input_dataset, coordinate_system)] = {
                x["priority"]: x["datastream_name"] for x in rule
            }
        return priorities

    @property
    def _transform_mappings(self) -> dict[str, str]:
        mappings = {}
        for input_dataset, coords in zip(
            self._get_transform_mappings().input_dataset.values,
            self._get_transform_mappings().coordinate_system.values,
        ):
            mappings[input_dataset] = coords
        return mappings

    def _get_output_mappings(self) -> pd.DataFrame:
        process = self.process_info
        df_stacked = pd.DataFrame(
            process["variable_retrieval"]["output_datastream_variable_mappings"]
        ).stack()
        df_var_output_mapping = df_stacked.reset_index()
        df_var_output_mapping.columns = [
            "variable",
            "output_datastream",
            "variable_out",
        ]  # non-standard names
        return pd.merge(
            df_var_output_mapping,
            pd.DataFrame(
                {"output_datastream": self.output_datastreams},
            ),
            how="outer",
        )

    def _get_retrieved_variables(self, rich_info: bool = False) -> pd.DataFrame:
        process = self.process_info
        df_var = pd.DataFrame(process["variable_retrieval"]["retrieved_variables"]).T
        df_var.index.name = "variable"  # non-standard names
        df_var = df_var.reset_index().sort_values("input_dataset")
        df_var = df_var.drop("name", axis=1).rename(
            lambda x: "retrieval_rule_set" if x == "input_dataset" else x,
            axis="columns",
        )
        if rich_info:
            return df_var
        else:
            return df_var[["variable", "retrieval_rule_set", "coordinate_system"]]

    def get_retrieval_rules(
        self, rich_info: bool = True, pivot: bool = True
    ) -> pd.DataFrame:
        if rich_info:
            df_retrieval_rule_set_rules = self._get_full_retrieval_rules()
        else:
            df_retrieval_rule_set_rules = self._get_filtered_retrieval_rules()

        df_retrieval_rule_set_rules_normalized = pd.concat(
            [
                df_retrieval_rule_set_rules.explode("rules").reset_index(drop=True),
                pd.json_normalize(
                    df_retrieval_rule_set_rules.explode("rules").rules,  # type: ignore
                    max_level=0,
                ),
            ],
            axis=1,
        ).drop("rules", axis=1)
        df_retrieval_rule_set_rules_normalized = (
            df_retrieval_rule_set_rules_normalized.sort_values(
                ["retrieval_rule_set", "priority"]
            )
        )
        if pivot:
            return self._pivot_df_by(
                df_retrieval_rule_set_rules_normalized,
                "retrieval_rule_set",
                index_within_group=True,
            )
        else:
            return df_retrieval_rule_set_rules_normalized

    @staticmethod
    def filter_dict(
        datastream: dict,
    ):
        filtered = [
            {
                key: datastream_dict[key]
                for key in [
                    "priority",
                    "datastream_name",
                    # "run_location",
                    # "run_time",,
                    # "data_location"
                ]
            }
            for datastream_dict in datastream
        ]
        return sorted(filtered, key=lambda d: d["priority"])

    def _get_full_retrieval_rules(self) -> pd.DataFrame:
        process = self.process_info
        return pd.DataFrame(
            pd.DataFrame(process["variable_retrieval"]["input_datasets"]).T["rules"]
        ).reset_index(names="retrieval_rule_set")

    def _get_filtered_retrieval_rules(self) -> pd.DataFrame:
        df = self._get_full_retrieval_rules()
        df["rules"] = df.rules.apply(self.filter_dict)
        return df

    def _get_filtered_retrieval_rule_set_rules(self) -> pd.DataFrame:
        df_filtered_retrieval_rules = self._get_filtered_retrieval_rules()
        df_filtered_retrieval_rules["input_datastreams"] = (
            df_filtered_retrieval_rules.rules.apply(
                lambda x: list(set([rule["datastream_name"] for rule in x]))
            )
        )
        return df_filtered_retrieval_rules

    def _get_mapping_rules(self):
        df_rules = self._get_filtered_retrieval_rule_set_rules()
        df_vars = self._get_retrieved_variables()

        return pd.merge(
            df_rules,
            df_vars,
            how="inner",
            on="retrieval_rule_set",
        ).drop("variable", axis=1)

    def _get_transform_mappings(self):
        df_rules = self._get_filtered_retrieval_rule_set_rules()
        df_vars = self._get_retrieved_variables()
        df_mappings = (
            df_vars.groupby("input_dataset")["coordinate_system"]
            .apply(list)
            .reset_index()
        )
        df_mappings["coordinate_system_nona"] = df_mappings.coordinate_system.apply(
            lambda x: [coord for coord in x if coord]
        )
        return pd.merge(
            df_rules,
            df_mappings,
            how="left",
            on="input_dataset",
        )

    def get_pcm_overview(
        self, pivot_by_col: str = "retrieval_rule_set", show_pivot_name: bool = False
    ) -> pd.DataFrame:
        """pivot_by_col in [
            "retrieval_rule_set",
            "coordinate_system",
            "output_datastream",
            "no_pivot"
        ]"""
        assert pivot_by_col in [
            "retrieval_rule_set",
            "coordinate_system",
            "output_datastream",
            "no_pivot",
        ]
        df = self._get_pcm_overview()
        if pivot_by_col == "no_pivot":
            return df
        elif pivot_by_col == "output_datastream":
            df_pivot = self._pivot_df_by(
                df.explode(pivot_by_col),  # type: ignore
                pivot_by_col,
                index_within_group=True,
            )
            if show_pivot_name:
                df_pivot.index.name = (pivot_by_col, "")
            return df_pivot
        else:
            df_pivot = self._pivot_df_by(df, pivot_by_col)
            if show_pivot_name:
                df_pivot.index.name = (pivot_by_col, "")
            return df_pivot

    @staticmethod
    def _pivot_df_by(
        df: pd.DataFrame, col: str, index_within_group: bool = False
    ) -> pd.DataFrame:
        df_pivot = df.copy()
        df_pivot = df_pivot.sort_values(col).reset_index(drop=True)
        if not index_within_group:
            single_index = df_pivot.index
        else:
            single_index = pd.Index(
                df_pivot.fillna("NA").groupby(col).cumcount().values
            )
        tuples = zip(df_pivot[col], single_index)
        index = pd.MultiIndex.from_tuples(
            tuples,
            names=[col, single_index.name],
        )
        df_pivot.index = index
        df_pivot = df_pivot.drop([col], axis=1)
        return df_pivot

    def _get_pcm_overview(self) -> pd.DataFrame:
        df_var_non_rich = self._get_retrieved_variables()
        df_output_mapping = (
            self._get_output_mappings()
            .groupby("variable")
            .output_datastream.apply(list)
            .reset_index()
        )
        df_input_dataset_rules_non_normalized = (
            self._get_filtered_retrieval_rule_set_rules()
        )

        df_merge_1 = pd.merge(
            df_var_non_rich, df_output_mapping, how="outer", on="variable"
        )
        df_merge_2 = pd.merge(
            df_merge_1,
            df_input_dataset_rules_non_normalized,
            how="outer",
            on="retrieval_rule_set",
        )

        return (
            df_merge_2[
                [
                    "retrieval_rule_set",
                    "coordinate_system",
                    "variable",
                    "output_datastream",
                    "rules",
                ]
            ]
            .sort_values(["retrieval_rule_set", "coordinate_system", "variable"])
            .reset_index(drop=True)
        )


@dataclass
class DataShelf:
    # TODO: future: support .shape, .keys, length, etc.

    def __post_init__(self):
        # Configure ADI Environment variables,
        self._data: list[dict[str, xr.Dataset | None]] = []
        # self._ts: list[dict[str, tuple[int, int] | None]] = []
        self._ts: list[tuple[int, int] | None] = []

    def append_interval(
        self,
        interval_data: dict[str, xr.Dataset | None],
        interval_ts: tuple[int, int] | None,
    ) -> DataShelf:
        self._data.append(interval_data)
        self._ts.append(interval_ts)
        return self

    # def += method  # TODO: def += method

    def __getitem__(self, key: int | str) -> DataSubShelf:
        # TODO: future: support slicing
        if isinstance(key, int):
            return self.by_interval(key)
        elif isinstance(key, str):
            return self.by_datastream(key)
        else:
            raise

    def by_datastream(self, name: str) -> DataSubShelf:
        # return [x[name] for x in self.data]
        return DataSubShelf(
            [x[name] for x in self._data],
            [x for x in self._ts],
            name,
        )

    def by_interval(self, index: int) -> DataSubShelf:
        # return self.data[index]
        return DataSubShelf(self._data[index], self._ts[index], index)

    def _per_interval_repr(
        self,
        # ts_dict: dict[str, tuple[int, int] | None],
        ts_tuple: tuple[int, int] | None,
        data_dict: dict[str, xr.Dataset | None],
    ):
        if ts_tuple:
            begin = datetime.datetime.fromtimestamp(ts_tuple[0]).strftime("%Y-%m-%d")
            end = datetime.datetime.fromtimestamp(ts_tuple[1]).strftime("%Y-%m-%d")
        else:
            begin = "0000-00-00"
            end = "0000-00-00"
        time_stamp_line = "\t" + f"{begin}--> {end}" + "\t{"

        dataset_lines: list[str] = []
        for datastream, ds in data_dict.items():
            # dim_info = ", ".join([f"{k}: {v}" for k, v in ds.sizes.items()])
            dataset_lines += [
                "\t\t" + f"{datastream}: {XarrayDatasetRepr.one_line_repr(ds)},"
            ]

        close_line = "\t}"

        return [time_stamp_line] + dataset_lines + [close_line]

    def __repr__(self):
        """
        EXAMPLE:
        DataStore
        [
            <0/2> 	2022-01-01--> 2022-01-02	{
                adimappedgrid.c1: xr.Dataset(time: 1440, bound: 2),
                adiregulargrid.c1: xr.Dataset(time: 48, range: 8000, bound: 2),
                nocoord.c1: xr.Dataset(time: 1440, bound: 2),
                nocoord2.c1: xr.Dataset(time: 1440, bound: 2),
            }
            <1/2> 	2022-01-02--> 2022-01-03	{
                adimappedgrid.c1: xr.Dataset(time: 1440, bound: 2),
                adiregulargrid.c1: xr.Dataset(time: 48, range: 8000, bound: 2),
                nocoord.c1: xr.Dataset(time: 1440, bound: 2),
                nocoord2.c1: xr.Dataset(time: 1440, bound: 2),
            }
            <2/2> 	2022-01-03--> 2022-01-04	{
                adimappedgrid.c1: xr.Dataset(time: 1440, bound: 2),
                adiregulargrid.c1: xr.Dataset(time: 48, range: 8000, bound: 2),
                nocoord.c1: xr.Dataset(time: 1440, bound: 2),
                nocoord2.c1: xr.Dataset(time: 1440, bound: 2),
            }
        ]
        """
        open_lines = "DataStore\n["

        dataset_lines = []
        for i, (interval, data) in enumerate(zip(self._ts, self._data)):
            per_interval_repr = self._per_interval_repr(interval, data)
            per_interval_repr[0] = (
                "\t" + f"<{i}/{len(self._ts) - 1}+1> " + per_interval_repr[0]
            )
            # dataset_lines += per_interval_repr(interval, data)
            if i < 2 or (i == 2 and len(self._ts) <= 3):
                dataset_lines += per_interval_repr
            elif i == len(self._ts) - 1:
                dataset_lines += ["\n\t...\n"]
                dataset_lines += per_interval_repr

        close_line = "]"

        return "\n".join([open_lines] + dataset_lines + [close_line])


class DataSubShelf:
    # TODO: future: support .shape, .keys, length, etc.
    def __init__(self, data_slice, ts_slice, key):
        self.data_slice: list[xr.Dataset] | dict[str, xr.Dataset] = data_slice
        # self.ts_slice: list[tuple[int, int]] | dict[str, tuple[int, int]] = ts_slice
        self.ts_slice: list[tuple[int, int]] | tuple[int, int] = ts_slice
        self.key: str | int = key

    @staticmethod
    def _index_timestamp_expression(
        index: int, last_index: int, begin: int, end: int
    ) -> str:
        if last_index < 0:
            total_str = " "
        else:
            total_str = last_index
        t_begin = datetime.datetime.fromtimestamp(begin).strftime("%Y-%m-%d")
        t_end = datetime.datetime.fromtimestamp(end).strftime("%Y-%m-%d")
        return f"<{index}/{total_str}+1>" + "\t" + f"{t_begin}--> {t_end}"

    def _dict_like_repr(self):
        """
        EXAMPLE
        DataStore (interval=	<0/ >	2020-04-01--> 2020-04-02)
        {
            co2flx25m_b1: xr.Dataset(time: 48, bound: 2),
            swats_b1: xr.Dataset(time: 48, depth: 6),
        }
        """
        if (
            isinstance(self.ts_slice, tuple)
            and isinstance(self.data_slice, dict)
            and isinstance(self.key, int)
        ):
            # ts_slice: dict[str, tuple[int, int]] = self.ts_slice
            ts_slice: tuple[int, int] = self.ts_slice
            data_slice: dict[str, xr.Dataset] = self.data_slice
            key: int = self.key
        ts_tuple = ts_slice
        time_stamp_line = self._index_timestamp_expression(
            key,
            -1,
            ts_tuple[0],
            ts_tuple[1],
        )
        open_lines = [f"DataStore (interval=\t{time_stamp_line}) \n" + "{"]
        repr_body = [
            "\t" + f"{datastream}: {XarrayDatasetRepr.one_line_repr(ds)},"
            for datastream, ds in data_slice.items()
        ]

        close_line = ["}"]
        return open_lines + repr_body + close_line

    def _list_like_repr(self):
        """
        EXAMPLE:
        DataStore (datastream=	co2flx25m_b1)
        [
            <0/4>	2020-04-01--> 2020-04-02	xr.Dataset(time: 48, bound: 2),
            <1/4>	2020-04-02--> 2020-04-03	xr.Dataset(time: 48, bound: 2),

            ...

            <4/4>	2020-04-05--> 2020-04-06	xr.Dataset(time: 48, bound: 2),
        ]
        """

        if (
            isinstance(self.ts_slice, list)
            and isinstance(self.data_slice, list)
            and isinstance(self.key, str)
        ):
            ts_slice: list[tuple[int, int]] = self.ts_slice
            data_slice: list[xr.Dataset] = self.data_slice
            key: str = self.key
        open_lines = [f"DataStore (datastream=\t{key}) \n["]
        repr_body = []
        for i, (ts, ds) in enumerate(zip(ts_slice, data_slice)):
            per_interval_repr = [
                "\t"
                + self._index_timestamp_expression(
                    i,
                    len(self.data_slice) - 1,
                    ts[0],
                    ts[1],
                )
                + "\t"
                + XarrayDatasetRepr.one_line_repr(ds)
                + ","
            ]
            if i < 2 or (i == 2 and len(self.ts_slice) <= 3):
                repr_body += per_interval_repr
            elif i == len(self.ts_slice) - 1:
                repr_body += ["\n\t...\n"]
                repr_body += per_interval_repr
        close_line = ["]"]
        return open_lines + repr_body + close_line

    def __repr__(self):
        if isinstance(self.data_slice, list):
            return "\n".join(self._list_like_repr())
        else:
            return "\n".join(self._dict_like_repr())

    def __getitem__(self, key: int | str) -> xr.Dataset:
        # TODO: future: support slicing
        if isinstance(self.data_slice, dict) and isinstance(key, str):
            return self.data_slice[key]
        elif isinstance(self.data_slice, list) and isinstance(key, int):
            return self.data_slice[key]
        raise


class XarrayDatasetRepr:
    @staticmethod
    def one_line_repr(ds: xr.Dataset | None):
        if ds is not None:
            dim_info = ", ".join([f"{k}: {v}" for k, v in ds.sizes.items()])
            return f"xr.Dataset({dim_info})"
        else:
            return "NA"

    @staticmethod
    def get_xrdataset_info(ds: xr.Dataset):
        # TODO: discuss what other fundamental info should be put here
        attr_dod_version = {"dod_version": ds.attrs["dod_version"]}
        xr_dataset_info: dict = {
            "time range": f'({str(ds.time.data[0]).split(".")[0]}, {str(ds.time.data[-1]).split(".")[0]})',
            "Coordinates": str(list(ds.coords)),
            "Data variables": str(list(ds.data_vars)),
        }
        xr_dataset_info.update(attr_dod_version)
        return xr_dataset_info


# @dataclass
class ProcessStatus:
    """Basic class representing the final process state."""

    def __init__(self, logs: str = "", terminal_message: str = "") -> None:
        self._logs = logs
        self._terminal_message = terminal_message  # redirected from terminal

    @property
    def logs(self):
        return self._logs

    @property
    def terminal_message(self):
        return self._terminal_message

    def inject(self, logs: str = "", terminal_message: str = ""):
        self._logs += logs
        self._terminal_message += terminal_message

    def print_logs(self, show_terminal_message=True):
        if show_terminal_message and self._terminal_message:
            print(self._terminal_message)
        print(self.logs)

    def get_last_status(self) -> str:
        """
        ['Status:  No Output Data Created']
        EXAMPLE:
        >>
        "No Output Data Created"
        """
        line_logs = self._logs.splitlines()
        status_line = [line for line in line_logs if "Status:" in line]
        return " ".join(
            "".join(status_line[-1]).split()[1:]
        )  # TODO: refactor this, not readable. Goal: strip away the trailing "Status: "

    @staticmethod
    def patch_logs(logs: str, message: str = "Data Consolidate Mode: Successful."):
        """
        EXAMPLE:
        patch_status(logs, message="Data Consolidate Mode: Successful.")
        "Data Consolidate Mode: Succeed."
        >>
        ...\nStatus:  Data Consolidate Mode, Succeed.\n'"""
        return logs + f"Status:  {message}\n"

    def __repr__(self) -> str:
        return f"ProcessStatus={self.get_last_status()}"

    def __bool__(self) -> bool:
        return "Successful" in self.get_last_status()


@dataclass
class CacheReference:
    pcm_version: int = field(init=True)

    init_process_hook: str
    pre_retrieval_hook: str
    post_retrieval_hook: str
    pre_transform_hook: str
    post_transform_hook: str

    process_data_hook: str
    finish_process_hook: str
    quicklook_hook: str


class ProcessCache:
    def __init__(
        self,
        sys_argv: SysArgv,
        hook_manager: ProcessHookManager,
        cache_dir: str | None = None,
    ) -> None:
        self.sys_argv = sys_argv
        self.hook_manager = hook_manager
        self.pcm = PCM(self.sys_argv.process_name)

        self.pcm_version = self.pcm.revision_number

        self.init_process_hook = hook_manager.init_process_hook
        self.pre_retrieval_hook = hook_manager.pre_retrieval_hook
        self.post_retrieval_hook = hook_manager.post_retrieval_hook
        self.pre_transform_hook = hook_manager.pre_transform_hook
        self.post_transform_hook = hook_manager.post_transform_hook
        self.process_data_hook = hook_manager.process_data_hook
        self.finish_process_hook = hook_manager.finish_process_hook
        self.quicklook_hook = hook_manager.quicklook_hook

        if not cache_dir:
            cache_dir = os.environ.get("ADI_CACHE_DIR")
        self.pickle_path = f"{cache_dir}/{self.sys_argv.process_name}"

    @staticmethod
    def get_f_cont(f: Callable) -> str:
        return inspect.getsource(f)

    @staticmethod
    def get_func_annotations(f: Callable) -> dict:
        return inspect.get_annotations(f)

    def construct_pickle_path(
        self,
        begin: int = -1,
        end: int = -1,
        type: str = "type",
    ) -> str:
        """
        encoded pickle name that can identify if a process is run on consolidator per process interval."""
        # TODO: adding function encoding to tell if certain custom hook is injected and if the content has changed.
        pcm = self.sys_argv.process_name
        site = self.sys_argv.site
        facility = self.sys_argv.facility
        return os.path.join(
            self.pickle_path, f"{pcm}_{site}_{facility}_{begin}_{end}_{type}.pickle"
        )

    def _is_pcm_version_equal_to_local_reference(self):
        # check if pcm version is the same to local reference/cache
        return self.check_against_cached_reference(
            CONSTANT.PCM_VERSION, self.pcm_version
        )

    def _are_vap_preprocessing_hooks_equal_to_local_reference(self):
        # check if vap hooks are the same to local reference/cache
        target = [
            self.hook_manager.init_process_hook,
            self.hook_manager.pre_retrieval_hook,
            self.hook_manager.post_retrieval_hook,
            self.hook_manager.pre_transform_hook,
            self.hook_manager.post_transform_hook,
        ]
        return self.check_against_cached_reference(
            CONSTANT.VAP_PREPROCESSING_HOOKS, target
        )

    def check_against_cached_reference(self, type: str, target: Any | None) -> bool:
        # First check if reference exists, if not dump reference to local,
        # otherwise exists, compare if reference and target are equal
        cached_ref: Any = self.load_pickle_from_path(cache_type=type, raise_mode=False)
        if cached_ref:
            return cached_ref == target
        else:
            abs_path = self.construct_pickle_path(type=type)
            self.dump_var(abs_file=abs_path, var=target)
            return False

    def load_pickle_from_path(
        self,
        begin: int = -1,
        end: int = -1,
        cache_type: str = "type",
        raise_mode: bool = False,
    ) -> Any | None | int | ProcessHookManager:
        abs_file = self.construct_pickle_path(begin, end, cache_type)
        try:
            with open(abs_file, "rb+") as f:
                var = pickle.load(f)
            return var
        except Exception as e:
            # print(e)  # TODO: Using logger to control print
            if raise_mode:
                raise e

    def dump_pickle_to_path(
        self,
        var: Any,
        begin: int = -1,
        end: int = -1,
        cache_type: str = "type",
        raise_mode: bool = False,
    ):
        abs_file = self.construct_pickle_path(begin, end, cache_type)
        try:
            self.dump_var(abs_file, var)
        except Exception as e:
            print(e)
            if raise_mode:
                raise e

    @staticmethod
    def construct_pickle_name(
        pcm: str,
        version: str,
        site: str,
        facility: str,
        begin: int,
        end: int,
        cache_type: str,
    ):
        """
        encoded pickle name that can identify if a process is run on consolidator per process interval."""
        # TODO: adding function encoding to tell if certain custom hook is injected and if the content has changed.
        return f"{pcm}_{version}_{site}_{facility}_{begin}_{end}_{cache_type}.pickle"

    @staticmethod
    def dump_var(abs_file: str, var: dict[str, xr.Dataset | None] | Any):
        parent_path = pathlib.Path(abs_file).parents[0]
        Util.validate_output_path(str(parent_path))
        with open(abs_file, "wb+") as f:
            pickle.dump(var, f)

    @staticmethod
    def load_var(abs_file: str, raise_mode=False) -> dict[str, xr.Dataset | None] | Any:
        try:
            with open(abs_file, "rb+") as f:
                var = pickle.load(f)
            return var
        except Exception as e:
            if raise_mode:
                print(e)
                raise e

    @classmethod
    def clean_cache(cls): ...  # TODO


class ProcessWrapper(Process):
    def __init__(
        self,
        # process_name: str,
        sys_argv: SysArgv,
        process_hook_manager,  # type: setup_process_hook.ProcessHookManager
        # pcm: PCM,  # TODO: avoid passing this all around the place. implement singleton/cached pool to PCM
        smart_cache: bool = True,
        data_consolidate_mode: bool = False,
        # cache_dir=os.environ.get("ADI_CACHE_DIR"),
        *args,
        **kwargs,
    ):
        super().__init__()
        # self._process_name = process_name
        self.sys_argv = sys_argv
        self._process_name = self.sys_argv.process_name
        self.process_hook_manager = process_hook_manager  # type: setup_process_hook.ProcessHookManager
        self.process_cache = ProcessCache(
            self.sys_argv, self.process_hook_manager, os.environ.get("ADI_CACHE_DIR")
        )
        self.smart_cache = smart_cache
        self.data_consolidate_mode = data_consolidate_mode

        self.pickle_path = self.process_cache.pickle_path

        self._process_names = [self._process_name]
        self._include_debug_dumps = False

        self.pcm = PCM(self._process_name)
        # self.pcm = pcm

        self._input_datasets = None
        self._transformed_datasets = None
        self._output_placeholder_datasets = None
        self._output_datasets = None

        self.input_dataset_paths: list[tuple[str, tuple[int, int]]] = []
        self.transformed_dataset_paths: list[tuple[str, tuple[int, int]]] = []
        self.output_placeholder_dataset_paths: list[tuple[str, tuple[int, int]]] = []
        self.output_dataset_paths: list[tuple[str, tuple[int, int]]] = []

        self._interval_input = None
        self._interval_transformed = None
        self._interval_output_placeholder = None
        self._interval_output = None

        # self.current_interval: int = -1

        Util.validate_output_path(self.pickle_path)

    @property
    def input_datasets(self) -> DataShelf:  # type: ignore
        if self.input_dataset_paths == []:
            return DataShelf()
        elif self._input_datasets is not None:
            return self._input_datasets
        self._input_datasets = DataShelf()
        for interval_data_path, (begin_date, end_date) in self.input_dataset_paths:
            interval_data = ProcessCache.load_var(interval_data_path)
            self._input_datasets.append_interval(
                interval_data,
                (begin_date, end_date),
            )
        return self._input_datasets

    @property
    def transformed_datasets(self) -> DataShelf:  # type: ignore
        if self.transformed_dataset_paths == []:
            return DataShelf()
        elif self._transformed_datasets is not None:
            return self._transformed_datasets
        self._transformed_datasets = DataShelf()
        for interval_data_path, (
            begin_date,
            end_date,
        ) in self.transformed_dataset_paths:
            interval_data = ProcessCache.load_var(interval_data_path)
            self._transformed_datasets.append_interval(
                interval_data,
                (begin_date, end_date),
            )
        return self._transformed_datasets

    @property
    def output_placeholder_datasets(self) -> DataShelf:  # type: ignore
        if self.output_placeholder_dataset_paths == []:
            return DataShelf()
        elif self._output_placeholder_datasets is not None:
            return self._output_placeholder_datasets
        else:
            self._output_placeholder_datasets = DataShelf()
            for interval_data_path, (
                begin_date,
                end_date,
            ) in self.output_placeholder_dataset_paths:
                interval_data = ProcessCache.load_var(interval_data_path)
                self._output_placeholder_datasets.append_interval(
                    interval_data,
                    (begin_date, end_date),
                )
            return self._output_placeholder_datasets

    @property
    def output_datasets(self) -> DataShelf:  # type: ignore
        if self.output_dataset_paths == []:
            return DataShelf()
        elif self._output_datasets is not None:
            return self._output_datasets
        self._output_datasets = DataShelf()
        for interval_data_path, (
            begin_date,
            end_date,
        ) in self.output_dataset_paths:
            interval_data = ProcessCache.load_var(interval_data_path)
            self._output_datasets.append_interval(
                interval_data,
                (begin_date, end_date),
            )
        return self._output_datasets

    def get_interval_input_datasets(
        self,
    ) -> dict[str, xr.Dataset | None] | None:
        return deepcopy(self._interval_input)

    def get_interval_transformed_datasets(
        self,
    ) -> dict[str, xr.Dataset | None] | None:
        return deepcopy(self._interval_transformed)

    def get_interval_output_placeholder_datasets(
        self,
    ) -> dict[str, xr.Dataset | None] | None:
        return deepcopy(self._interval_output_placeholder)

    def sync_interval_datasets(self, interval_data: dict[str, xr.Dataset | None]):
        for k, v in interval_data.items():
            if v:
                self.sync_datasets(v)
                ADILogger.info(f"ADILogger.info: sync dataset of {k} in interval.")

    @property
    def process_name(self) -> str:
        """Overrides the error-prone parent method"""
        # return dsproc.get_name()
        return self._process_name

    @property
    def site(self) -> str:
        """Overrides the error-prone parent method"""
        return self._from_sys_args("-s")

    @property
    def facility(self) -> str:
        """Overrides the error-prone parent method"""
        return self._from_sys_args("-f")

    def init_process_hook(self):
        self.process_hook_manager.init_process_hook(self)

    def pre_retrieval_hook(self, begin_date: int, end_date: int):
        self.process_hook_manager.pre_retrieval_hook(self, begin_date, end_date)

    def post_retrieval_hook(self, begin_date: int, end_date: int):
        # Note: if no input data found per processing interval.
        # ADI would not enter the remaining hooks including this one.
        self.process_hook_manager.post_retrieval_hook(self, begin_date, end_date)

    def pre_transform_hook(self, begin_date: int, end_date: int):
        # Note: dsproc_merge_data hook can merge multiple data per interval,
        # thus better to retrieve input data in this hook, i.e.,
        # to avoid handing get_retrieved_dataset vs. get_retrieved_datasets.
        # ref: https://engineering.arm.gov/ADI_doc/algorithm.html?highlight=process%20model#dsproc-main
        self.process_hook_manager.pre_transform_hook(self, begin_date, end_date)
        if self.has_preprocessing:
            self._interval_input = self._update_datasets(
                begin_date, end_date, CONSTANT.PREPROCESSED_INPUT
            )
        else:
            self._interval_input = self._update_datasets(
                begin_date, end_date, CONSTANT.INPUT
            )

        # # TODO: here is the candidate place holder to directly inject custom code,
        # # to access it, use runner._input_datasets[index].
        # # Note: runner.input_datasets might not be available at this moment,
        # # since process_interval is not available until the later process hook.

        # # TODO: add and verify sync process

    def post_transform_hook(self, begin_date: int, end_date: int):
        self.process_hook_manager.post_transform_hook(self, begin_date, end_date)
        if self.has_preprocessing:
            self._interval_transformed = self._update_datasets(
                begin_date, end_date, CONSTANT.PREPROCESSED_TRANSFORMED
            )
        else:
            self._interval_transformed = self._update_datasets(
                begin_date, end_date, CONSTANT.TRANSFORMED
            )

    def process_data_hook(self, begin_date: int, end_date: int):
        if self.has_preprocessing:
            self._interval_output_placeholder = self._update_datasets(
                begin_date, end_date, CONSTANT.PREPROCESSED_OUTPUT_PLACEHOLDER
            )
        else:
            self._interval_output_placeholder = self._update_datasets(
                begin_date, end_date, CONSTANT.OUTPUT_PLACEHOLDER
            )
        self.process_hook_manager.process_data_hook(self, begin_date, end_date)
        self._interval_output = self._update_datasets(
            begin_date, end_date, CONSTANT.OUTPUT
        )

    def quicklook_hook(self, begin_date: int, end_date: int):
        self.process_hook_manager.quicklook_hook(self, begin_date, end_date)

    def finish_process_hook(self):
        self.process_hook_manager.finish_process_hook(self)

    def retrieve_per_interval_input_datasets(self):
        # TODO: this method is a good candidate to make a mock for developing.
        interval_data = {}
        for (
            input_dataset,
            priorities,
        ) in self.pcm.retrieval_rule_set_priorities.items():
            input_datastreams = priorities.values()
            for ds_name in input_datastreams:
                ds = self.get_retrieved_dataset(ds_name)
                if ds is not None:
                    ds = ds.copy(deep=True)
                    interval_data[input_dataset] = ds
                    break  # Break for datastream with lower priority
            if interval_data.get(input_dataset) is None:
                interval_data[input_dataset] = None  # place holder
        return interval_data

    def retrieve_per_interval_transformed_datasets(self):
        interval_data = {}
        for (
            (input_dataset, coordinate_system),
            priorities,
        ) in self.pcm.mapping_priorities.items():
            input_datastreams = priorities.values()
            # for coordinate_system in runner.pcm_process.transform_mappings[input_dataset]:
            mapping_name = PCM.construct_mapping(input_dataset, coordinate_system)
            if coordinate_system is None:
                continue
            for ds_name in input_datastreams:
                ds = self.get_transformed_dataset(ds_name, coordinate_system)
                if ds is not None:
                    ds = ds.copy(deep=True)

                    interval_data[mapping_name] = ds
                    break  # Break for datastream with lower priority
            if interval_data.get(mapping_name) is None:
                interval_data[mapping_name] = None  # place holder
        return interval_data

    def retrieve_per_interval_output_datasets(self):
        interval_data = {}
        for ds_name in self.pcm.output_datastreams:
            ds = self.get_output_dataset(ds_name)
            if ds is not None:
                ds = ds.copy(deep=True)
                interval_data[ds_name] = ds
            else:
                interval_data[ds_name] = ds
        return interval_data

    @staticmethod
    def _from_sys_args(key: str):
        """
        Note: only support retrieve site (-s), facility (-f), begin_date (-b), end_date (-e)
        EXAMPLE:
        _from_sys_args(key = "-b")
        >> {begin_date}
        """
        assert key in ["-s", "-f", "-b", "-e"]
        args = sys.argv
        return [args[i + 1] for i, e in enumerate(args) if e == key][0]

    def invoke_vap_class_hook(
        self,
        hook_name: str,
        *hook_args: Any,
        **hook_kwargs: Any,
    ) -> None:
        hook = getattr(self.process_hook_manager.process_class_type, hook_name)
        hook(self, *hook_args, **hook_kwargs)
        return None

    @property
    def has_preprocessing(self) -> bool:
        """Check if there is any hook for preprocessing different from those in adi_py.Process class"""
        return any(
            [
                self.process_hook_manager.init_process_hook
                != Process.init_process_hook,
                self.process_hook_manager.pre_retrieval_hook
                != Process.pre_retrieval_hook,
                self.process_hook_manager.post_retrieval_hook
                != Process.post_retrieval_hook,
                self.process_hook_manager.pre_transform_hook
                != Process.pre_transform_hook,
                self.process_hook_manager.post_transform_hook
                != Process.post_transform_hook,
            ]
        )

    def _update_datasets(
        self, begin_date: int, end_date: int, cache_type: str
    ) -> dict[str, xr.Dataset | None]:
        """
        Mechanism to load datasets from local cache or using adi_py utility
        """
        begin_date = int(begin_date)  # Note: parsing from C code
        end_date = int(end_date)
        interval_data: dict[str, xr.Dataset | None]
        loaded_cache = self.process_cache.load_pickle_from_path(
            begin_date, end_date, cache_type
        )
        # TODO: handle caching preprocessed hook != Process.pre_transform_hook
        if (
            loaded_cache is not None
            and self.process_cache._is_pcm_version_equal_to_local_reference()
            and self.process_cache._are_vap_preprocessing_hooks_equal_to_local_reference()
            and self.smart_cache
            and cache_type != CONSTANT.OUTPUT
        ):
            interval_data = loaded_cache  # type: ignore
            ADILogger.info(f"Found cached file and using for {cache_type=}.")
        else:
            if cache_type in [CONSTANT.INPUT, CONSTANT.PREPROCESSED_INPUT]:
                interval_data = self.retrieve_per_interval_input_datasets()
            elif cache_type in [
                CONSTANT.TRANSFORMED,
                CONSTANT.PREPROCESSED_TRANSFORMED,
            ]:
                interval_data = self.retrieve_per_interval_transformed_datasets()
            elif cache_type in [
                CONSTANT.OUTPUT_PLACEHOLDER,
                CONSTANT.PREPROCESSED_OUTPUT_PLACEHOLDER,
            ]:
                interval_data = self.retrieve_per_interval_output_datasets()
            elif cache_type in [
                CONSTANT.OUTPUT,
            ]:
                interval_data = self.retrieve_per_interval_output_datasets()
            else:
                pass
                raise ValueError(f"{cache_type=} not support here.")
            self.process_cache.dump_pickle_to_path(
                interval_data, begin_date, end_date, cache_type
            )
        interval_data_path = self.process_cache.construct_pickle_path(
            begin=begin_date, end=end_date, type=cache_type
        )
        if cache_type in [CONSTANT.INPUT, CONSTANT.PREPROCESSED_INPUT]:
            self.input_dataset_paths.append(
                (interval_data_path, (begin_date, end_date))
            )
        elif cache_type in [
            CONSTANT.TRANSFORMED,
            CONSTANT.PREPROCESSED_TRANSFORMED,
        ]:
            self.transformed_dataset_paths.append(
                (interval_data_path, (begin_date, end_date))
            )
        elif cache_type in [
            CONSTANT.OUTPUT_PLACEHOLDER,
            CONSTANT.PREPROCESSED_OUTPUT_PLACEHOLDER,
        ]:
            self.output_placeholder_dataset_paths.append(
                (interval_data_path, (begin_date, end_date))
            )
        elif cache_type == CONSTANT.OUTPUT:
            self.output_dataset_paths.append(
                (interval_data_path, (begin_date, end_date))
            )

        return interval_data


def setup_process_hook(adi_runner: AdiRunner):
    @dataclass
    class ProcessHookManager:
        # process_class_type: type[Process] = field(default=Process, repr=False)
        init_process_hook: Callable = field(default=Process.init_process_hook)
        pre_retrieval_hook: Callable = field(default=Process.pre_retrieval_hook)
        post_retrieval_hook: Callable = field(default=Process.post_retrieval_hook)
        pre_transform_hook: Callable = field(default=Process.pre_transform_hook)
        post_transform_hook: Callable = field(default=Process.post_transform_hook)
        process_data_hook: Callable = field(default=Process.process_data_hook)
        finish_process_hook: Callable = field(default=Process.finish_process_hook)
        quicklook_hook: Callable = field(default=Process.quicklook_hook)

        def __post_init__(self):
            self._setup_process_hooks()

        def _setup_process_hooks(self):
            """Helper function to setup process hooks,
            Precedence: 1. API inputs of the defined process_class hooks as a group,
                        2. API inputs of the defined hooks mixed with reasonable default (i.e., adi_py.Process class).
                        3. Default: adi_py.Process hooks
            Then update the instance fields accordingly"""
            hook_names = [
                "init_process_hook",
                "pre_retrieval_hook",
                "post_retrieval_hook",
                "pre_transform_hook",
                "post_transform_hook",
                "process_data_hook",
                "finish_process_hook",
                "quicklook_hook",
            ]
            for hook_name in hook_names:
                if adi_runner.process_class_type != Process and getattr(
                    adi_runner, hook_name
                ) != getattr(Process, hook_name):
                    # TODO: discuss should this be raise instead?
                    msg = (
                        f"Warning: The provided process_class '{adi_runner.process_class_type}' implements {hook_name}"
                        f", but {hook_name} was also provided as an argument to the {self.__class__.__name__} API. The"
                        f" group of hooks in process_class '{adi_runner.process_class_type}' will be used, and the individual"
                        f" hook argument '{hook_name}' will be discarded."
                    )
                    print(msg)
                    # revert to the clean state: CustomProcessClass.hooks
                    setattr(
                        self,
                        hook_name,
                        getattr(adi_runner.process_class_type, hook_name),
                    )
                    setattr(
                        adi_runner,
                        hook_name,
                        getattr(adi_runner.process_class_type, hook_name),
                    )
                elif adi_runner.process_class_type != Process:
                    # CustomProcessClass.hooks
                    setattr(
                        self,
                        hook_name,
                        getattr(adi_runner.process_class_type, hook_name),
                    )
                    setattr(
                        adi_runner,
                        hook_name,
                        getattr(adi_runner.process_class_type, hook_name),
                    )
                else:  # individual custom hooks
                    setattr(
                        self,
                        hook_name,
                        getattr(adi_runner, hook_name),
                    )
                self._validate_process_hook()

        def _validate_process_hook(
            self,
        ): ...  # TODO

        def print_hook_content(self, hook_name: str):
            ...
            # TODO: using inspect

    return ProcessHookManager()


@dataclass
class ProcessMock:
    input_datasets: DataShelf = field(default=DataShelf(), repr=False)
    transformed_datasets: DataShelf = field(default=DataShelf(), repr=False)
    output_placeholder_datasets: DataShelf = field(default=DataShelf(), repr=False)

    # def __init__(
    #     self,
    #     input_datasets: DataShelf = DataShelf(),
    #     transformed_datasets: DataShelf = DataShelf(),
    #     output_placeholder_datasets: DataShelf = DataShelf(),
    # ) -> None:
    #     self._input_datasets = input_datasets
    #     self._transformed_datasets = transformed_datasets
    #     self._output_placeholder_datasets = output_placeholder_datasets

    def __post_init__(self):
        self._default_index = 0
        self._dummy_input_datasets = deepcopy(self.input_datasets)
        self._dummy_transformed_datasets = deepcopy(self.transformed_datasets)
        self._dummy_output_placeholder_datasets = deepcopy(
            self.output_placeholder_datasets
        )

    def set_default_index(self, i: int):
        if i <= len(self.input_datasets._data) and i >= 0:
            self._default_index = i

    @property
    def default_index(self) -> int:
        return self._default_index

    def print_pre_transform_hook_example(self): ...

    def print_process_data_hook_example(self): ...

    def get_interval_input_datasets(
        self,
    ) -> dict[str, xr.Dataset | None] | DataSubShelf:
        self._validate_datasets_access()
        # return self.input_datasets._data[self.default_index]
        self._dummy_input_datasets = deepcopy(self.input_datasets)
        return self._dummy_input_datasets[self.default_index]

    def get_interval_transformed_datasets(
        self,
    ) -> dict[str, xr.Dataset | None] | DataSubShelf:
        # return self.transformed_datasets._data[self.default_index]
        # return self.transformed_datasets[self.default_index]
        self._dummy_transformed_datasets = deepcopy(self.transformed_datasets)
        return self._dummy_transformed_datasets[self.default_index]

    def get_interval_output_placeholder_datasets(
        self,
    ) -> dict[str, xr.Dataset | None] | DataSubShelf:
        # return self.output_placeholder_datasets._data[self.default_index]
        # return self.output_placeholder_datasets[self.default_index]
        self._dummy_output_placeholder_datasets = deepcopy(
            self.output_placeholder_datasets
        )
        return self._dummy_output_placeholder_datasets[self.default_index]

    def sync_interval_datasets(
        self, interval_data: dict[str, xr.Dataset | None] | DataSubShelf
    ): ...  # TODO: verify the original sync_interval_datasets

    def _validate_datasets_access(self): ...  # TODO

    def validate_custom_hook(self, custom_hook: Callable):
        ...
        # TODO: static/dynamic check
        # func name
        # func para
        # return
        #

    def unit_test_processed_interval_data(
        self,
        custom_hook: Callable,
    ) -> dict[str, dict[str, xr.Dataset | None] | DataSubShelf]:
        """
        Utility to unit-test custom hook. Return the processed interval data
        """
        self.validate_custom_hook(custom_hook)
        custom_hook(self, begin_date=-1, end_date=-1)
        return {
            CONSTANT.INPUT: self._dummy_input_datasets[self.default_index],
            CONSTANT.TRANSFORMED: self._dummy_transformed_datasets[self.default_index],
            CONSTANT.OUTPUT_PLACEHOLDER: self._dummy_output_placeholder_datasets[
                self.default_index
            ],
        }  # type: ignore
