import pathlib
import shutil
import sys
from typing import List
from enum import IntEnum


class Select(IntEnum):
    DIR = 1
    FILE = DIR << 1
    ALL = (DIR << 2) - 1


class DirSync:
    def __init__(self, src: pathlib.Path, dst: pathlib.Path, ignore: List[str] = None,
                 selected: Select = Select.ALL, verbose=False):
        assert src.exists(), "Source does not exist."
        assert dst.exists(), "Destination does not exist."

        self.src = src
        self.dst = dst
        self.ignore = list()
        if ignore is not None:
            self.ignore = [i.lower() for i in ignore]
        self.selected = selected
        self.verbose = verbose

    def sync(self, dir_rel: pathlib.Path = None):
        if dir_rel is not None:
            src = self.src / dir_rel
            dst = self.dst / dir_rel
        else:
            src = self.src
            dst = self.dst
            dir_rel = self.src

        if self.verbose:
            sys.stderr.write("Sync " + str(dir_rel) + '\n')

        for dir_child in src.iterdir():
            if dir_child.name.lower() in self.ignore:
                continue
            if dir_child.is_dir():
                if not (dst / dir_child.name).exists() and self.selected & Select.DIR:
                    sys.stderr.write("Copy " + str(dir_child.relative_to(self.src)) + '\n')
                    shutil.copytree(str(src / dir_child.name), str(dst / dir_child.name))
                else:
                    dir_rel_child = (dir_rel / dir_child).relative_to(self.src)
                    self.sync(dir_rel=dir_rel_child)
            elif dir_child.is_file() and self.selected & Select.FILE:
                if not (dst / dir_child.name).exists() and dst.exists():
                    sys.stderr.write("Copy " + str(dir_child.relative_to(self.src)) + '\n')
                    shutil.copy(str(src / dir_child.name), str(dst / dir_child.name))


def main():
    src = input("Source: ")
    dst = input("Destination: ")

    src_p = pathlib.Path(src).resolve()
    dst_p = pathlib.Path(dst).resolve()

    ds = DirSync(src_p, dst_p)
    ds.sync()


if __name__ == "__main__":
    main()