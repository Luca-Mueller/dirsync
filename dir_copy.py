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
            self.ignore = ignore
        self.selected = selected
        self.verbose = verbose

    def sync_dir(self, dir_rel: pathlib.Path):
        src = self.src / dir_rel
        dst = self.dst / dir_rel

        if self.verbose:
            sys.stderr.write("Sync " + str(dir_rel) + '\n')

        for dir_child in src.iterdir():
            if dir_child.name in self.ignore:
                continue
            if dir_child.is_dir():
                if not (dst / dir_child.name).exists() and self.selected & Select.DIR:
                    sys.stderr.write("Copy " + str(dir_child) + '\n')
                    shutil.copytree(str(src / dir_child.name), str(dst / dir_child.name))
                else:
                    dir_rel_child = (dir_rel / dir_child).relative_to(self.src)
                    self.sync_dir(dir_rel_child)
            elif dir_child.is_file() and self.selected & Select.FILE:
                if not (dst / dir_child.name).exists():
                    sys.stderr.write("Copy " + str(dir_child) + '\n')
                    shutil.copy(str(src / dir_child.name), str(dst / dir_child.name))

    def sync(self):
        for dir_child in self.src.iterdir():
            if dir_child.name in self.ignore:
                continue
            if dir_child.is_dir():
                if not (self.dst / dir_child.name).exists() and self.selected & Select.DIR:
                    shutil.copytree(str(self.src / dir_child.name), str(self.dst / dir_child.name))
                else:
                    dir_rel = dir_child.relative_to(self.src)
                    self.sync_dir(dir_rel)
            elif dir_child.is_file() and self.selected & Select.FILE:
                shutil.copy(str(self.src / dir_child.name), str(self.dst / dir_child.name))
        print("Done!")


def main():
    src = input("Source: ")
    dst = input("Destination: ")

    src_p = pathlib.Path(src).resolve()
    dst_p = pathlib.Path(dst).resolve()

    ds = DirSync(src_p, dst_p)
    ds.sync()


if __name__ == "__main__":
    main()