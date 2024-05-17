from pathlib import Path
import collections
import json
import os
import tempfile
import typing
import zipfile

from oj.testcase import TestCase


class Problem:
    def __init__(self, title: str) -> None:
        self.title = title
        self.spj = False
        self.testcases: typing.Dict[str, TestCase] = collections.defaultdict(TestCase)

    def extract_as_dir(self, dirname: typing.Optional[str]=None, in_ext='.in', out_ext='.out', info='info') -> None:
        """Save problem in a directory.

        dirname: default is `./PROBLEM_TITLE`
        """
        dir_path = Path(dirname) if dirname is not None else Path(f'./{self.title}')
        data = {
            "spj": self.spj,
            "testcases": {},
        }
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for id, tc in self.testcases.items():
            input_name = id+in_ext
            output_name = id+out_ext
            with open(dir_path / input_name, 'w') as f:
                f.write(tc.input_text)
            with open(dir_path / output_name, 'w') as f:
                f.write(tc.output_text)
            data['testcases'][id] = {
                "stripped_output_md5": tc.stripped_output_md5,
                "input_size": tc.input_size,
                "output_size": tc.output_size,
                "input_name": input_name,
                "output_name": output_name,
            }
        with open(dir_path / info, 'w') as f:
            json.dump(data, f, ensure_ascii=True)

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
