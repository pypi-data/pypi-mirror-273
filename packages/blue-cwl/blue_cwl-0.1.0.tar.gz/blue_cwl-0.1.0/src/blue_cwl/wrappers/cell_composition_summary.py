"""Cell composition summary app."""

import logging
from pathlib import Path

import click
from voxcell.nexus.voxelbrain import LocalAtlas

from blue_cwl import registering, staging, statistics, utils

L = logging.getLogger(__name__)


@click.group()
def app():
    """The CLI object."""


@app.command()
@click.option("--atlas-release", help="Atlas release KG resource id.", required=True)
@click.option("--density-distribution", help="Density distribution KG dataset id.", required=True)
@click.option("--output-dir", required=True)
def from_density_distribution(
    atlas_release,
    density_distribution,
    output_dir,
):
    """Calculate summary statistics from density distribution."""
    output_dir = utils.create_dir(output_dir)

    atlas_dir = utils.create_dir(output_dir / "atlas")
    staging.stage_atlas(
        atlas_release,
        output_dir=atlas_dir,
        parcellation_ontology_basename="hierarchy.json",
        parcellation_volume_basename="brain_regions.nrrd",
    )
    atlas = LocalAtlas.open(str(atlas_dir))

    density_distribution_file = Path(output_dir / "density_distribution.parquet")

    densities = staging.materialize_cell_composition_volume(
        density_distribution,
        output_file=density_distribution_file,
    )

    composition_summary_file = output_dir / "cell_composition_summary.json"
    _run_summary(
        dataset=densities,
        atlas=atlas,
        output_file=composition_summary_file,
    )

    # pylint: disable=no-member
    registering.register_cell_composition_summary(
        name="Cell composition summary",
        summary_file=composition_summary_file,
        atlas_release_id=atlas_release,
        derivation_entity_id=density_distribution,
    )


def _run_summary(dataset, atlas, output_file):
    summary = statistics.atlas_densities_composition_summary(
        density_distribution=dataset,
        region_map=atlas.load_region_map(),
        brain_regions=atlas.load_data("brain_regions"),
        map_function="auto",
    )
    utils.write_json(filepath=output_file, data=summary)
