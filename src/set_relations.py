from dataclasses import dataclass
from relation import IDK, K, Relation2, Term, isomorphism
from result import Result2, Result3
from typing import Dict, Generic, Hashable, Set, Tuple, TypeVar
from enum import Enum, auto

H = TypeVar('H', bound=Hashable)

def union(a_term: Term[Set[H]], b_term: Term[Set[H]], out_term: Term[Set[H]]) -> Result3[Set[H], Set[H], Set[H]]: # TODO
    match a_term, b_term, out_term:
        case K(a), K(b), K(out):
            pass

        case K(a), K(b), IDK():
            pass

        case K(a), IDK(), K(out):
            pass

        case K(a), IDK(), IDK():
            pass

        case IDK(), K(b), K(out):
            pass

        case IDK(), K(b), IDK():
            pass

        case IDK(), IDK(), K(out):
            pass

        case IDK(), IDK(), IDK():
            pass

def subset(subset_term: Term[Set[H]], superset_term: Term[Set[H]]) -> Result2[Set[H], Set[H]]:
    match subset_term, superset_term:
        case K(subset), K(superset):
            pass

        case K(subset), IDK():
            pass

        case IDK(), K(superset):
            pass

        case IDK(), IDK():
            pass

def strict_subset(subset_term: Term[Set[H]], superset_term: [Term[Set[H]]]) -> Result2[Set[H], Set[H]]:
    match subset_term, superset_term:
        case K(subset), K(superset):
            pass

        case K(subset), IDK():
            pass

        case IDK(), K(superset):
            pass

        case IDK(), IDK():
            pass


class VennDiagram(Enum):
    ONLY_IN_LEFT  = auto()
    ONLY_IN_RIGHT = auto()
    IN_BOTH       = auto()


def pair_to_venn_diagram(pair: Tuple[Set[H], Set[H]]) -> Dict[H, VennDiagram]:
    left, right = pair

    venn_diagram: Dict[H, VennDiagram] = {}
    for x in left.union(right):
        if x in left and x in right: venn_diagram[x] = VennDiagram.IN_BOTH
        elif x in left:              venn_diagram[x] = VennDiagram.ONLY_IN_LEFT
        elif             x in right: venn_diagram[x] = VennDiagram.ONLY_IN_RIGHT

    return venn_diagram
    

def venn_diagram_to_pair(venn_diagram: Dict[H, VennDiagram]) -> Tuple[Set[H], Set[H]]:
    left: Set[H] = set()
    right: Set[H] = set()

    for x in venn_diagram:
        match venn_diagram[x]:
            case VennDiagram.IN_BOTH:      left.add(x) ; right.add(x)
            case VennDiagram.ONLY_IN_LEFT: left.add(x)
            case VennDiagram.ONLY_IN_RIGHT:              right.add(x)

    return left, right


venn_diagram = isomorphism("venn_diagram", pair_to_venn_diagram, venn_diagram_to_pair)

@dataclass
class VennDiagramWithUniverse(Generic[H]):
    in_left:    Set[H]
    in_right:   Set[H]
    in_both:    Set[H]
    in_neither: Set[H]