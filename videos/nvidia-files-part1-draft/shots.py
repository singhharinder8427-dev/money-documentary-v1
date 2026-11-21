"""DRAFT runner for The Nvidia Files Part 1 (silent, estimated timing until the owner's narration exists).
Uses the real shot list in ../nvidia-files-part1/shots.py."""
import importlib.util, pathlib
_p = pathlib.Path(__file__).resolve().parent.parent / 'nvidia-files-part1' / 'shots.py'
_s = importlib.util.spec_from_file_location('nf1', _p); M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
SHOT_BREAKS = M.SHOT_BREAKS
build = M.build
