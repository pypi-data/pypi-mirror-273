from typing import Literal, Optional, Sequence

import numpy as np
import pandas as pd

from .species import Species

from gprofiler import GProfiler
import aiohttp
import asyncio
import nest_asyncio

# for JupyterNotebook support
nest_asyncio.apply()


class DIOPTRelease:
    """
    Util class for fetching orthologs.
    """

    _gp = GProfiler(return_dataframe=True)

    def __init__(
        self, version: Literal["v8", "v9"] = "v8", input_species: str | int = "human"
    ) -> None:
        if version not in ["v8", "v9"]:
            if version in [8, 9]:
                self.version = f"v{version}"
            else:
                raise TypeError("The version annot be parsed. Please indicate whether v8 or v9 is to be used")
        else:
            if version == "v9":
                print(
                    "Please note that v9 is currently in beta testing. Use v8 if you prefer the stable version."
                )
            self.version = version

        try:
            self.input_species = Species.parse_species(input_species, error=True)
        except:
            raise ValueError(
                "The input species cannot be parsed. Refer to pyDIOPT.Species.available() for a complete list of supported species."
            )

    def fetch(
        self,
        genes: Sequence[str],
        target_species: Optional[Species | str | int],
        filter: Optional[
            Literal["best_match", "exclude_score_less_1", "exclude_score_less_2"]
        ] = None,
        condensed: bool = True,
    ) -> pd.DataFrame:
        """
        Queries the DIOPT RESTful API endpoint for orthologs.

        You can theoretically fetch information for all annotated species by passing in None for target species, but just so you know it will be a lot slower.

        By default, only select information will be returned in the output pd.DataFrame. If comprehensive information is desired, pass in condensed=False. Note this action is both memory and time consuming.
        """

        def url_builder(
            api_version: str,
            input_species: int,
            target_species: Optional[int],
            filter: str,
        ):
            return (
                lambda entrez_gene_id: f"https://www.flyrnai.org/tools/diopt/web/diopt_api/{api_version}/get_orthologs_from_entrez/{input_species}/{entrez_gene_id}/{target_species if target_species else 'all'}/{filter}"
            )

        target_species_id = (
            Species.parse_species(target_species).ncbi_taxonomy_id
            if target_species
            else "all"
        )

        base = url_builder(
            self.version,
            self.input_species.ncbi_taxonomy_id,
            target_species_id,
            filter if filter else "none",
        )

        genes = self.convert_to_entrez_acc(genes)

        async def _fetch(session, url):
            async with session.get(url) as response:
                try:
                    return await response.json()
                except:
                    raise ValueError(
                        f"The returned data cannot be deserialized.\nQuery: {url}\nResponse: {response}"
                    )

        async def _fetch_all(urls):
            async with aiohttp.ClientSession() as session:
                tasks = []
                for url in urls:
                    task = asyncio.create_task(_fetch(session, url))
                    tasks.append(task)
                results = await asyncio.gather(*tasks)
                return results

        results = asyncio.run(_fetch_all([base(gene) for gene in genes]))

        unmatched = []
        chunks = []

        for entry in results:
            try:
                gene_details = entry["search_details"]["gene_details"][0]
            except:
                print(
                    f'entry["search_details"]["gene_details"] is {entry["search_details"]["gene_details"]}. entry is {entry}'
                )

            if not entry["results"]:
                unmatched.append(gene_details["symbol"])
                continue

            for i in entry["results"].values():
                if condensed:
                    chunk = pd.DataFrame(i.values())[
                        [
                            "species_id",
                            "symbol",
                            "geneid",
                            "species_specific_geneid",
                            "species_specific_geneid_type",
                            "confidence",
                        ]
                    ]
                    chunk = chunk.add_prefix("target_")
                    chunk.insert(0, "input_symbol", gene_details["symbol"])
                    chunk.insert(
                        1, "input_ensembl_geneid", gene_details["ensembl_geneid"]
                    )
                else:
                    chunk = pd.DataFrame(i.values())
                    chunk = chunk.add_prefix("target_")
                    chunk = chunk.assign(
                        **{f"input_{key}": value for key, value in gene_details.items()}
                    )
                chunks.append(chunk)

        if unmatched:
            print(
                f"{np.ceil(len(unmatched) / len(genes) * 100)}% of the queries are returned unmatched:\n{unmatched}"
            )

        return (
            pd.concat(chunks, axis=0, ignore_index=True) if chunks else pd.DataFrame()
        )

    def convert_to_entrez_acc(self, genes: Sequence[str]) -> np.array:
        """
        Helper function that converts a list of arbitrary gene identifiers to Entrez IDs using the gprofiler library.

        Theoretically the list of genes can be in any format but it should preferabbly be passed in as a list, np.ndarray, or pd.Series.

        Returns an np.array of the Entrez IDs. If the full pd.DataFrame is desired, use the gprofiler library directly.
        """
        organism = self.input_species.latin_name.split(" ")
        organism = (organism[0][0] + organism[1]).lower()

        result = self._gp.convert(
            organism=organism.lower(),
            query=list(np.array(genes).tolist()),
            target_namespace=(
                "ENTREZGENE_ACC" if organism != "dmelanogaster" else "ENTREZGENE"
            ),
        )

        if result[result["converted"] == "None"].shape[0]:
            print(
                f'The following queries ({np.ceil(result[result["converted"] == "None"].shape[0] / len(genes) * 100)}%) returned None when trying to get Entrez Acc Number:\n{result[result["converted"] == "None"]["incoming"].tolist()}'
            )

        return result[result["converted"] != "None"]["converted"].to_numpy()
