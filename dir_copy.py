import pathlib
import shutil
import sys


#TODO:
# - determine source and destination
# - copy dir if not there, else switch to dir & repeat (for all directories)
#   sync src, dst:
#       for dir in src:
#           if not dir.exists(dst) -> dir.copy(src, dst)
#           else -> sync src/dir, dst/dir


class DirSync:
    def __init__(self, src: pathlib.Path, dst: pathlib.Path, verbose=False):
        assert src.exists(), "Source does not exist."
        assert dst.exists(), "Destination does not exist."

        self.src = src
        self.dst = dst
        self.verbose = verbose

    def sync_dir(self, dir_rel: pathlib.Path):
        src = self.src / dir_rel
        dst = self.dst / dir_rel

        if self.verbose:
            sys.stderr.write("Sync " + str(dir_rel) + '\n')

        for dir_child in src.iterdir():
            if dir_child.is_dir():
                if not (dst / dir_child.name).exists():
                    print("Copy " + str(dir_child))
                    shutil.copytree((src / dir_child.name), (dst / dir_child.name))
                else:
                    dir_rel_child = (dir_rel / dir_child).relative_to(self.src)
                    self.sync_dir(dir_rel_child)

    def sync(self):
        for item in self.src.iterdir():
            if item.is_dir():
                dir_rel = item.relative_to(self.src)
                self.sync_dir(dir_rel)
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