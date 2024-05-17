import calling_rate

import inspect
import json
import os
import typer

cli = typer.Typer()


@cli.command()
def write_initial_population(
    bootstrapping_number: int = typer.Option(),
    output_path: str = typer.Option(),
    burrow_jm_data_path: str = typer.Option(),
    burrow_geci_data_path: str = typer.Option(),
    calling_numbers_data_path: str = typer.Option(),
):

    paths = {
        "recorders_data": calling_numbers_data_path,
        "geci_data": burrow_geci_data_path,
        "jm_data": burrow_jm_data_path,
    }
    ratecalling_burrow_data = calling_rate.RateCalling_Burrow_Data(paths, B=bootstrapping_number)
    interval = ratecalling_burrow_data.get_bootstrapped_number_of_burrows_in_recorder_area()
    dict_to_write = {
        "b_number": bootstrapping_number,
        "intervals": list(interval),
        "data_sources": paths,
        "get": get_command_reference(),
    }
    with open(output_path, "w") as jsonfile:
        json.dump(dict_to_write, jsonfile)


def get_command_reference():
    command_name = inspect.stack()[1][3]
    return (
        calling_rate.__name__ + "." + os.path.basename(__file__).split(".")[0] + ":" + command_name
    )


@cli.command()
def version():
    version = calling_rate.__version__
    print(version)
