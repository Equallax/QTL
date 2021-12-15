from os.path import isfile
from tkinter.filedialog import askopenfilename
from typing import Iterable, Iterator, Tuple

from scipy.stats import ttest_ind

from concentration_reader import parse_concentrations
from read_markers import Marker, parse_markers


def split_concentrations(concentrations: Iterable, marker_scores: Iterable) -> Tuple[list, list]:
    """Separates the inputted concentrations into two lists. The first one containing the values of plants
    that got a band. The second list contains all values from plants that didn't get a band. Both arguments have to be
    of equal length.

    Args:
        concentrations: List of concentrations of every plant.
        marker_scores: List containing strings of value a,b or a dash(-).

    Returns:
        Tuple of separated concentration values.
    """
    band = []
    no_band = []
    for score, concentration in zip(marker_scores, concentrations):
        if score == "b":
            band.append(concentration)
        elif score == "a":
            no_band.append(concentration)
    return band, no_band


def test_marker(marker: Marker, concentrations: Iterable) -> Tuple[str, float]:
    """Returns the name and significance of a marker. Arguments have to be of equal length.

    Args:
        marker: A single Marker instance.
        concentrations: All concentrations of plants that have been analysed with the marker.

    Returns:
        Name of marker and p-value.
    """
    group1, group2 = split_concentrations(concentrations, marker.scores)
    return marker.name, ttest_ind(group1, group2)[1]


def test_markers(markers: Iterable[Marker], concentrations: Iterable, alpha: float = 0.05) -> Iterator:
    """Returns the name and significance of a marker. Arguments have to be of equal length.

        Args:
            markers: Iterable containing Marker instances.
            concentrations: All concentrations of plants that have been analysed with the markers.
            alpha: P-value cutoff. Defaults to 0.05 .

        Returns:
            Name of marker and p-value.
        """
    marker_p_value_pairs = []
    for marker in markers:
        marker_p_value_pairs.append(test_marker(marker, concentrations))

    marker_p_value_pairs.sort(key=lambda x: x[1])
    return [*(filter(lambda x: x[1] <= alpha, marker_p_value_pairs))]


def get_safe_filename(filename: str) -> str:
    """Returns filename with the lowest integer possible at the end if filename is already used.

    Args:
        filename: Filename that is to be checked.

    Returns:
        Safe filename.
    """

    counter = 0
    filename_list = filename.split(".")
    filename_list[-2] += "{}."

    template_filename = "".join(filename_list)
    while isfile(template_filename.format(counter if counter else "")):
        counter += 1

    return template_filename.format(counter if counter else "")


def save_as_table(iterable: Iterable[Iterable], delimiter: str = ';') -> None:
    """Saves an iterable as a table.

    Args:
        iterable: An iterable object.
        delimiter: String to separate colomns with.

    Returns:
        None
    """

    with open(get_safe_filename("output.table"), 'w+') as table_file:
        for row in iterable:
            table_file.write(delimiter.join((str(element) for element in row)) + "\n")


def main():
    concentration_file = askopenfilename(filetypes=[("Concentration files", "*.qua")])
    marker_file = askopenfilename(filetypes=[("Marker files", "*.loc")])

    concentrations_list = parse_concentrations(concentration_file)
    marker_list = parse_markers(marker_file)
    save_as_table(test_markers(marker_list, concentrations_list))


if __name__ == '__main__':
    main()
