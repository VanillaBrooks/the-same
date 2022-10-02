import json
import csv
from typing import Dict, Union, Optional

# factor to multiply the number of occurances of `the same` by
# to exaggerate the thickness of the edge
EDGE_SCALING_FACTOR = 3;

class Node():
    def __init__(self, name: str):
        self.name = name
    
    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.name,
            "group": 0
        }

    def __repr__(self) -> str:
        return f"{self.name}"

    def has_name(self, name: str):
        return self.name.lower() == name.lower()


class Edge():
    def __init__(self, person_one: str, person_two: str, reason: str):
        self.person_one = person_one
        self.person_two = person_two

        self.reasons : list[str] = [reason]
    
    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "source": self.person_one,
            "target": self.person_two,
            "value": len(self.reasons) * EDGE_SCALING_FACTOR 
        }

    # check that the names match, without including case
    def is_match(self, p1: str, p2: str) -> bool:
        p1 = p1.lower()
        p2 = p2.lower()

        a = self.person_one.lower()
        b = self.person_two.lower()

        return (p1 == a and p2 == b) or (p2 == a and p1 == b)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def __repr__(self) -> str:
        return f"{self.person_one}/{self.person_two}/{len(self.reasons)}"


def nodes_contain_name(node_list: list[Node], name: str) -> bool:
    return next(filter(lambda x: x.has_name(name), node_list), None) is not None

def find_edge(edge_list: list[Edge], person_one: str, person_two: str) -> Optional[Edge]:
    return next(filter(lambda x: x.is_match(person_one, person_two), edge_list), None)


# this file must be run from the root directory of the project to correctly open the 
f = open("./the_same.csv", "r");
reader = csv.reader(f)

# skip the first line in the iterator since
# it only contains the column information
next(reader)



nodes : list[Node] =[]
edges: list[Edge] =[]


for row in reader:
    person_one = row[0]
    person_two = row[1]
    reason = row[2]

    # create nodes for people if they do not already exist
    if not (nodes_contain_name(nodes, person_one)):
        nodes.append(Node(person_one))

    if not (nodes_contain_name(nodes, person_two)):
        nodes.append(Node(person_two))

    edge = find_edge(edges, person_one, person_two)

    if edge is not None:
        edge.add_reason(reason)
    else:
        edges.append(Edge(person_one, person_two, reason))
    
output_json = {
    "nodes": [node.to_dict() for node in nodes],
    "links": [link.to_dict() for link in edges],
}


with open("./src/output.json", "w") as f:
    json.dump(output_json, f)
