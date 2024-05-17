from typing import Optional, Union


class Species:
    def __init__(
        self,
        latin_name: str,
        common_name: Optional[str | list[str]],
        ncbi_taxonomy_id: int,
    ) -> None:
        self.latin_name = latin_name
        self.common_name = common_name
        self.ncbi_taxonomy_id = ncbi_taxonomy_id
        self.registered: bool = False

    def __str__(self) -> str:
        return self.latin_name

    latin_name_map: dict[str, "Species"] = {}
    common_name_map: dict[str, "Species"] = {}
    ncbi_taxonomy_id_map: dict[int, "Species"] = {}

    @staticmethod
    def _register(species: "Species") -> None:
        """Intended for internal use only. Registers a species"""
        Species.latin_name_map[species.latin_name] = species
        if species.common_name:
            if type(species.common_name) == list:
                for common_name in species.common_name:
                    Species.common_name_map[common_name] = species
            else:
                Species.common_name_map[species.common_name] = species
        Species.ncbi_taxonomy_id_map[species.ncbi_taxonomy_id] = species

        species.registered = True

    @staticmethod
    def parse_species(
        search_query: Union["Species", str, int], error: bool = False
    ) -> "Species":
        """
        Returns the appropriate species object based on search query.

        A species object can also be passed in and the registered copy will be returned.

        Parameters:
            search_query: str | int | Species - any input that points to a species
            error: bool - whether to throw error if unable to parse species from search_query
        """

        if type(search_query) == int:
            if search_query in Species.ncbi_taxonomy_id_map:
                return Species.ncbi_taxonomy_id_map[search_query]
            else:
                message = f"NCBI Taxonomy id not found: {search_query}. A list of available species can be retrived by calling Species.available()."
                if error:
                    raise TypeError(message)
                else:
                    print(message)
        else:
            # if it is a registered species, return the species directly
            if type(search_query) == Species and search_query.registered:
                return search_query

            search_string = str(search_query).lower()

            # try matching common names first
            if search_string in Species.common_name_map:
                return Species.common_name_map[search_string]

            # try matching latin names directly
            search_string = search_string.capitalize()

            if search_string in Species.latin_name_map:
                return Species.latin_name_map[search_string]

            # try matching abbreviated latin names
            species_query = search_string.split(" ")[-1]
            for genus_species in Species.latin_name_map.keys():
                if species_query == genus_species.split(" ")[-1]:
                    return Species.latin_name_map[genus_species]

            message = f"Name not found: {search_query}. A list of available species can be retrived by calling Species.available()"
            if error:
                raise TypeError(message)
            else:
                print(message)

    @staticmethod
    def available() -> None:
        print("Available species through DIOPT:")
        for ncbi_taxnomoy_id, species in Species.ncbi_taxonomy_id_map.items():
            print(f"{ncbi_taxnomoy_id}\t{species.latin_name}")


Species._register(Species("Escherichia coli", common_name=None, ncbi_taxonomy_id=83333))
Species._register(Species("Arabidopsis thaliana", ["thale cress", "cress"], 3702))
Species._register(Species("Schizosaccharomyces pombe", "fission yeast", 4896))
Species._register(Species("Saccharomyces cerevisiae", ["budding yeast", "yeast"], 4932))
Species._register(Species("Caenorhabditis elegans", ["worm", "nematode"], 6239))
Species._register(Species("Anopheles gambiae", "mosquito", 7165))
Species._register(Species("Drosophila melanogaster", ["fly", "fruit fly"], 7227))
Species._register(Species("Danio rerio", "zebrafish", 7955))
Species._register(Species("Xenopus tropicalis", "western clawed frog", 8364))
Species._register(Species("Rattus norvegicus", ["rat", "brown rat"], 10116))
Species._register(Species("Mus musculus", "mouse", 10090))
Species._register(Species("Homo sapiens", "human", 9606))
