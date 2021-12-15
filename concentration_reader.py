/**
Copyright 2021 Dariush Mirkarimi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
**/

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
