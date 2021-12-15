from dataclasses import dataclass, field
from typing import Iterable, List


@dataclass
class Marker:
    name: str = ""
    _scores: list = field(default_factory=list, init=False)

    def __getitem__(self, item):
        return self._scores[item]

    def __len__(self):
        len(self._scores)

    def __iter__(self):
        return iter(self._scores)

    @property
    def scores(self):
        return self._scores

    def add_score(self, new_scores: Iterable):
        self._scores.append(new_scores)

    def add_scores(self, new_scores: Iterable):
        self._scores.extend(new_scores)


def parse_markers(file_path: str) -> List[Marker]:
    """Returns a list of Marker objects after parsing .loc file.

    Args:
        file_path: Path to .loc file

    Returns:
        List of Marker objects.
    """
    with open(file_path, "r") as f:
        marker_list = []

        for raw_line in f:
            split_line = raw_line.split(" ")
            if len(split_line) == 4:
                marker = Marker(split_line[0])
                break

        for raw_line in f:
            if raw_line.strip() == "":
                marker_list.append(marker)
                break

            if raw_line[0:2] != "  ":
                # Marker has been found
                marker_list.append(marker)

                marker = Marker(raw_line.split(" ")[0])
            else:
                scores = raw_line.replace(" ", "").strip()
                marker.add_scores(scores)

        return marker_list
