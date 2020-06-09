import itertools
import os
import sys
from modulefinder import Module
from typing import List, Set, Tuple

import grimp
import networkx as nx
import typer
from grimp import DirectImport
from grimp.adaptors.importscanner import ImportScanner
from grimp.application.config import settings
from impulse.application.use_cases import draw_graph


class OverrideableImportScanner(ImportScanner):
    def scan_for_imports(self, module: Module) -> Set[DirectImport]:
        imports = super().scan_for_imports(module)
        return {imp for imp in imports if not imp.line_contents.endswith("# nocycle")}


settings.configure(IMPORT_SCANNER_CLASS=OverrideableImportScanner)


def find_package_cycles(module_name: str, display: bool = False) -> None:
    sys.path.insert(0, os.getcwd())
    module = grimp.Module(module_name)
    import_graph = grimp.build_graph(module.package_name)

    def package_graph(package_name: str) -> nx.DiGraph:
        nx_graph = nx.DiGraph()
        children = import_graph.find_children(package_name)
        for child in children:
            nx_graph.add_node(child)

        # Dependencies between children.
        for upstream, downstream in itertools.permutations(children, r=2):
            if import_graph.direct_import_exists(imported=upstream, importer=downstream, as_packages=True):
                nx_graph.add_edge(upstream, downstream)
        return nx_graph

    stack = [module_name]
    while stack:
        name = stack.pop()
        graph = package_graph(name)
        try:
            cycle = nx.find_cycle(graph, orientation="original")
        except nx.NetworkXNoCycle:
            for module_child in sorted(graph.nodes):
                stack.append(module_child)
        else:
            typer.secho("Package import cycle detected:", fg="red", bold=True)
            typer.secho(cycle_repr(cycle), fg="red")
            if display:
                draw_graph(name)
            sys.exit(1)
    typer.secho(
        f"Success: no package import cycles detected in {len(import_graph.modules)} modules", fg="green", bold=True
    )


def cycle_repr(cycle: List[Tuple[str, str, str]]) -> str:
    return "\n-> ".join(e[0] for e in cycle + [cycle[0]])


if __name__ == "__main__":
    typer.run(find_package_cycles)
