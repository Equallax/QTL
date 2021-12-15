from typing import List


def parse_concentrations(file_path: str) -> List[float]:
    """Reads all concentrations from .qua file.

    Args:
        file_path: Path to .qua file.

    Returns:
        List of concentrations.
    """
    plants_list = []
    with open(file_path, 'r') as concentration_file:
        for line in concentration_file:
            split_line = line.split("\t")

            try:
                concentration = float(split_line[1])
                plants_list.append(concentration)

            except (ValueError, IndexError):
                pass

        return plants_list
