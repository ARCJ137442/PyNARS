# Tested legacy PyNARS fixture

`fixture/pynars` preserves the source used by the BabelNAR compatibility probe.
It differs from the newer dev baseline; do not substitute dev sources and claim the same tested model.
Run `python -u -m pynars.ConsolePlus` with working directory `vnars/fixture`.
Generated pickle caches, compiled extensions and Python bytecode are excluded.
The first construction rebuilds rule maps. Before API use, prewarm from vnars/fixture:
`python -c "from pynars.NARS.Control.Reasoner import Reasoner; Reasoner(100,100)"`.
Dependency setup and host process ownership live in ARCJ137442/vNARS.
Provider contract and verification: [vNARS CIN guide](https://github.com/ARCJ137442/vNARS/blob/main/docs/cin-guide.md).
