from pyDIOPT.species import Species
import pytest


def test_available():
    assert Species.available() == None


def test_number_of_species():
    assert len(Species.ncbi_taxonomy_id_map) == 12


def test_individual_organisms():
    e_coli = Species.parse_species("Escherichia coli")
    # test lower case & abbr
    assert Species.parse_species("e coli") == e_coli
    # test dot abbr
    assert Species.parse_species("E. coli") == e_coli
    # test species with the same name are not equal unless registered
    assert (
        Species("Escherichia coli", common_name=None, ncbi_taxonomy_id=83333) != e_coli
    )

    assert Species.parse_species("error") == None

    with pytest.raises(Exception):
        Species.parse_species("error", error=True)
