from pathlib import Path
import json
import os
import tempfile
import typing
import zipfile

from testcase import TestCase


class Problem:
    def __init__(self, title: str) -> None:
        self.title = title
        self.spj = False
        self.testcases: typing.Dict[str, TestCase] = {}

    def add_testcase(self, testcase: TestCase):
        """Add a testcase for this problem."""
        self.testcases[testcase] = testcase

    def extract_as_dir(self, dirname: typing.Optional[str]=None, in_ext='.in', out_ext='.out') -> None:
        """Save problem in a directory.

        dirname: default is `./PROBLEM_TITLE`
        """
        dir_path = Path(dirname) if dirname is not None else Path(f'./{self.title}')
        info_filename = 'info'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for testcase in self.testcases.values():
            testcase.input.extract_as_file(dir_path / (testcase.id+in_ext))
            testcase.output.extract_as_file(dir_path / (testcase.id+out_ext))
        with open(dir_path / info_filename, 'w') as f:
            json.dump({
                "spj": self.spj,
                "testcases": {
                    testcase.id: {
                        "stripped_output_md5": testcase.stripped_output_md5,
                        "input_size": testcase.input_size,
                        "output_size": testcase.output_size,
                        "input_name": (testcase.id+in_ext),
                        "output_name": (testcase.id+out_ext),
                    } for testcase in self.testcases.values()
                },
            }, f, ensure_ascii=True)

    def extract_as_zip(self, filename: typing.Optional[str]=None) -> None:
        """Save problem as .zip file

        filename: default is `./PROBLEM_TITLE.zip`
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = Path(filename) if filename is not None else Path(f'./{self.title}.zip')
            dir_path = Path(tmp_dir)
            self.extract_as_dir(dir_path)
            with zipfile.ZipFile(zip_path, 'w') as fzip:
                for basename in os.listdir(dir_path):
                    fzip.write(filename=dir_path/basename, arcname=basename)