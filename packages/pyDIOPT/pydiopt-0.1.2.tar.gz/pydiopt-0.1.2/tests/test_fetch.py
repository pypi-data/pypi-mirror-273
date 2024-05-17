import pytest

from pyDIOPT.fetch import DIOPTRelease


def test_init():
    with pytest.raises(ValueError):
        DIOPTRelease("v8", "not_a_species_name")

    assert DIOPTRelease(8)
    assert DIOPTRelease(9)

    with pytest.raises(TypeError):
        DIOPTRelease("v10")


def test_fetch(sample_hsapiens_genes):
    release = DIOPTRelease()

    sample_mouse_orthologs = release.fetch(
        sample_hsapiens_genes, target_species="mouse"
    )["target_symbol"].unique()

    assert "Apoa1" in sample_mouse_orthologs
    assert "Brca1" in sample_mouse_orthologs

    sample_orthologs = release.fetch(sample_hsapiens_genes, target_species=None)[
        "target_symbol"
    ].unique()

    assert len(sample_orthologs) >= len(sample_mouse_orthologs)
