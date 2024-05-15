import glob
import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess

import polars as pl

from pycrux.pipes import drop_row_that_is_all_null
from pycrux.utils.logger import logger


class Crux:
    def __init__(self, crux_common_root_folder: str):
        root = Path(os.path.expanduser(crux_common_root_folder))
        self._raise_if_folder_does_not_exist(root)
        self.root: Path = root
        self._bin_crFitTool: Path = (
            self.root / """tools/crFitTool/bin/crFitTool"""
        )

    def read_fit(
        self,
        fit_file: str,
        to_log: bool = False,
        ending: str = ".records.csv",
        clean: bool = False,
        move_to_folder: bool = False,
        folder_suffix: str = "_csv",
    ) -> pl.DataFrame:
        """Return the records for a given .fit file.

        Parameters
        ----------
        fit_file : str
            Path to a .fit file.
        to_log : bool, optional
            Whether or not to log information, by default False
        ending : str, optional
            Suffix that `crux` appends to the .fit files, by default ".records.csv"
        cleanup: bool, optional
            Whether or not to remove the .csv file after reading it, by default False

        Returns
        -------
        pl.DataFrame
            A `polars` data frame containing the records data.
        """
        self.crfittool(fit_file=fit_file, to_log=to_log)
        df = pl.read_csv(fit_file + ending).pipe(drop_row_that_is_all_null)
        if clean:
            self.cleanup(fit_file)
        else:
            if move_to_folder:
                self.move_to_folder(fit_file, folder_suffix)
        return df

    def move_to_folder(self, fit_file: str, folder_suffix: str) -> None:
        """Moves the created .csv files to a folder.

        Parameters
        ----------
        fit_file : str
            The name of the .fit file.
        folder_suffix : str
            The suffix to append to the folder name.
        """
        file = Path(os.path.expanduser(fit_file))
        # remove the .fit and add the suffix
        folder = file.with_suffix("").as_posix() + folder_suffix

        # try to create the folder if it does not exist
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass

        for created_file in glob.glob(f"{file}.*.csv"):
            # Move file
            try:
                os.rename(
                    created_file,
                    os.path.join(folder, os.path.basename(created_file)),
                )
            except Exception as e:
                logger.error(f"Could not move {created_file}: {e}")

    def cleanup(self, fit_file: str) -> None:
        """Remove the .csv file created by `crFitTool`.

        Parameters
        ----------
        fit_file : str
            The name of the .fit file.
        """
        file = Path(os.path.expanduser(fit_file))

        # Get all files of the format `fit_file.*.csv`.
        for created_file in glob.glob(f"{file}.*.csv"):
            # Try to safely remove the file.
            try:
                os.remove(created_file)
            except Exception as e:
                logger.error(f"Could not remove {created_file}: {e}")

    def read_fit_recursively(
        self, root: str, to_log: bool = True, ending: str = ".records.csv"
    ) -> dict[str, pl.DataFrame]:
        """Runs read_fit on all .fit files found recursively inside the root folder.

        Parameters
        ----------
        root : str
            Root folder in which to look for .fit files.
        to_log : bool, optional
            Whether or not to log information, by default True
        ending : str, optional
            Suffix that `crux` appends to the .fit files, by default ".records.csv"

        Returns
        -------
        dict[str, pl.DataFrame]
            A dictionary where the keys are the location of the .fit files, and
            the items are the data frames containing the records.
        """
        fit_files = self.get_all_files_in_folder(root)
        dict_of_dataframes: dict[str, pl.DataFrame] = {}
        for fit_file in fit_files:
            try:
                df = self.read_fit(
                    fit_file=fit_file, to_log=to_log, ending=ending
                )
                dict_of_dataframes[fit_file] = df
            except Exception as e:
                logger.error(f"Could not parse {fit_file}: {e}")
        return dict_of_dataframes

    def crfittool(
        self, fit_file: str, to_log: bool = False
    ) -> CompletedProcess[str]:
        """Run crFitTool.

        Parameters
        ----------
        fit_file : str
            The .fit file to parse.
        to_log : bool, optional
            Whether or not to log information, by default False

        Returns
        -------
        CompletedProcess[str]
            Information from `subprocess` including the command that was run
            and the stderr.

        Raises
        ------
        Exception
            Raises an exception if `fit_file` is not a .fit file.
        """
        if not fit_file.endswith("fit"):
            raise ValueError(f"Can only parse .fit files, got {fit_file}")

        file = Path(os.path.expanduser(fit_file))
        self._raise_if_file_does_not_exist(file)

        f = file.as_posix()
        command = f"""{self._bin_crFitTool} --in "{f}" --csv "{f}" """
        if to_log:
            logger.info(f"Running: {command}")
        result = subprocess.run(
            [command], shell=True, capture_output=True, text=True
        )
        if to_log:
            logger.info(result)
        return result

    def crfittool_recursively(
        self, root: str, to_log: bool = True
    ) -> list[CompletedProcess[str]]:
        """Run crfittool on all .fit files inside a folder.

        Parameters
        ----------
        root : str
            The folder in which to look for .fit files.
        to_log : bool, optional
            Whether or not to log information, by default False

        Returns
        -------
        list[CompletedProcess[str]]
            Information from `subprocess` including the command that was run
            and the stderr. Each element of the list is related to a .fit file.
        """
        # TODO: Use multiprocessing in the for-loop below.
        #       Should be an easy 4x-8x speedup.
        fit_files = self.get_all_files_in_folder(root)

        results = []
        for i, fit_file in enumerate(fit_files):
            if to_log:
                logger.info(f"Processing file {i} of {len(fit_files)}.")

            try:
                result = self.crfittool(fit_file, to_log)
                results.append(result)
            except Exception as e:
                logger.error(e)
        return results

    def get_all_files_in_folder(
        self,
        root: str,
        ending: str = ".fit",
    ) -> list[str]:
        """Returns the paths to all files with a specific ending inside a folder.

        Parameters
        ----------
        root : str
            The folder in which to (recursively) look for files.
        ending : str, optional
            The ending to match, by default ".fit"

        Returns
        -------
        list[str]
            A list containing all files found (recursively) inside the root folder.
        """
        sub_folders = [
            os.path.join(root_dir, sub_dir)
            for (root_dir, dirs, _) in os.walk(root)
            for sub_dir in dirs
        ]

        # Extension needs the starting dot.
        if ending[0] != ".":
            ending = "." + ending

        # Get all files with desired ending.
        fit_files_subdirs = [
            file
            for sub_folder in sub_folders
            for file in glob.glob(f"{sub_folder}/*{ending}")
        ]
        fit_files_root = glob.glob(f"""{root}/*{ending}""")
        return fit_files_root + fit_files_subdirs

    @staticmethod
    def _raise_if_file_does_not_exist(file: Path) -> None:
        if not file.is_file():
            raise FileNotFoundError(
                f"No file exists at the location specified: {file.as_posix()}"
            )

    @staticmethod
    def _raise_if_folder_does_not_exist(folder: Path) -> None:
        if not folder.is_dir():
            raise FileNotFoundError(
                f"No folder exists at the location specified: {folder.as_posix()}"
            )
