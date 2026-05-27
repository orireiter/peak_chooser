from scipy import signal
import click
import pandas
import matplotlib.pyplot as plt
import matplotlib.axes

TIME_INDEX = 0
CONTENT_INDEX = 1


def get_sample(file_path: str, delimiter: str | None = None) -> pandas.DataFrame:
    return pandas.read_csv(file_path, delimiter=delimiter)


def get_plots() -> list[matplotlib.axes.Axes]:
    _, axs = plt.subplots(1, 2, figsize=(12, 6))

    for ax in axs:
        ax.grid(True)
        ax.axhline(0, color="black", linewidth=1.2)

    return axs


@click.command()
@click.argument(
    "csv_path", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option(
    "--delimiter",
    "-d",
    default="\t",
    help="Delimiter used in the CSV file. Defaults to tab '\\t'.",
)
@click.option(
    "--prominence",
    type=click.FLOAT,
    default=None,
    help="Find peaks that are at least {PROMINENCE} higher than their surroundings.",
)
@click.option(
    "--distance",
    type=click.INT,
    default=None,
    help="Find peaks that are at least {DISTANCE} data points apart from each other.",
)
@click.option(
    "--detrend",
    is_flag=True,
    help="Normalize values around 0",
)
@click.option(
    "--plot",
    is_flag=True,
    help="Include this flag to display the visualization plots.",
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["echo", "csv"], case_sensitive=False),
    default="echo",
    help="Output format for the detected peaks. Defaults to 'echo'.",
)
def main(csv_path, delimiter, prominence, distance, detrend, plot, output):
    sample = get_sample(csv_path, delimiter)
    time_column_name = sample.columns[TIME_INDEX]
    content_column_name = sample.columns[CONTENT_INDEX]

    content_values = sample.iloc[:, CONTENT_INDEX]

    if detrend:
        content_values = signal.detrend(content_values)

    peak_indices, _ = signal.find_peaks(
        content_values, prominence=prominence, distance=distance
    )

    if detrend:
        peaks = []
        for idx in peak_indices:
            peaks.append(
                {
                    time_column_name: sample.iloc[idx, TIME_INDEX],
                    content_column_name: content_values[idx],
                }
            )
        peaks = pandas.DataFrame(peaks)
    else:
        peaks = sample.iloc[peak_indices]

    if peaks.empty:
        if output.lower() == "echo":
            click.echo("\n--- No Detected Peaks ---")

        return

    if output.lower() == "csv":
        click.echo(peaks.to_csv(index=False, lineterminator="\n"))
    else:
        click.echo("\n--- Detected Peaks ---")
        click.echo(peaks)

    if plot:
        plots = get_plots()

        plots[0].plot(sample.iloc[:, TIME_INDEX], content_values)

        plots[1].plot(
            peaks.iloc[:, TIME_INDEX],
            peaks.iloc[:, CONTENT_INDEX],
            marker="o",
            color="red",
            label="peaks",
        )

        plots[0].plot(
            peaks.iloc[:, TIME_INDEX],
            peaks.iloc[:, CONTENT_INDEX],
            marker="o",
            linestyle="--",
            color="red",
            label="peaks",
        )

        for p in plots:
            p.set_xlabel(sample.columns[TIME_INDEX])
            p.set_ylabel(sample.columns[CONTENT_INDEX])
            p.legend()

        plt.show()


if __name__ == "__main__":
    main()
