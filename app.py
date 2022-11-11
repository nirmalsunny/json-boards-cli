import typer
from os import path
import glob
import json
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

"""
This script tries to achieve the following tasks:
    -Combine all board lists inside the JSON files into a single JSON output
    -Order the board list alphabetically first by vendor, and then by name
    -Include metadata in the JSON output under a _metadata object including:
        -The total number of unique vendors
        -The total number of boards
    -Output the resultant JSON

@author Nirmal Sunny
"""
welcome_message = "\n A CLI application to combine all board lists inside the JSON files into a single JSON output.\n"

app = typer.Typer(help=welcome_message)


@app.callback()
def main():
    """
    A basic command to show helpful information.
    """

    typer.secho(
        welcome_message,
        fg=typer.colors.WHITE,
        bg=typer.colors.YELLOW,
    )
    print("\n Use the merge command to combine json files from 'boards' folder.")
    print("\n --file-path argument can be used to specify another directory.")


# 'merge' command initialization
@app.command("merge")
def merge(file_path: str = "boards"):
    """
    JSON files from a given directory using the --file-path option are combined into a single output.
    If no directory is provided, the default directory 'boards' is used.

    An example JSON file for this program may look like this:
    {
        "boards": [
            {
            "name": "D4-200S",
            "vendor": "Boards R Us",
            "core": "Cortex-M4",
            "has_wifi": false
            }
        ]
    }

    A JSON file without the 'boards' object will be ignored.
    """
    
    # Check if the path is valid
    if not path.isdir(file_path):
        typer.secho(
            f"Invalid Directory! Please choose a valid folder",
            fg=typer.colors.WHITE,
            bg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    # Clean the trailing slashes
    file_path.rstrip("/\\")

    # Add the wildcard pattern to find all json files
    file_path = file_path + "/**/*.json"

    # Find the JSON files from the given or default folder recursively
    json_files = glob.glob(file_path, recursive=True)

    # Define variables to hold the boards' data and the number of json files found
    boards = []
    valid_json_file_counter = 0

    # A progress bar is loaded while each json file is opened,
    # read, converted to an object and appended to the 'boards' list.

    # Invalid files and json without the 'boards' object are ignored.
    # Only valid board is added to the list.
    with typer.progressbar(json_files, label="Validating the JSON files") as progress:
        for json_file in progress:
            with open(json_file) as f:
                # Read the file
                contents = f.read()
                # Transform content into JSON object
                json_content = json.loads(contents)
                # If 'boards' exists, append it to the list
                if json_content["boards"]:
                    valid_json_file_counter += 1
                    for board in json_content["boards"]:
                        boards.append(board)

    # Output early hints that the program was able to find these factors.
    print(f"{len(boards)} boards found from {valid_json_file_counter} JSON files.")

    # Show spinner progress while sorting, printing and saving
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        # Add the spinner progress for sorting
        task_1 = progress.add_task(description="Sorting the Boards...", total=None)
        # Order the board list alphabetically first by vendor, and then by name
        sorted_boards = sorted(boards, key=lambda row: (row["vendor"], row["name"]))
        # Since sorting might be fairly quick, add delay for the animation to be visible
        time.sleep(1)
        # Let the progress know that the sorting has been finished
        progress.advance(task_1)

        task_2 = progress.add_task(description="Printing the Result...", total=None)
        time.sleep(1)
        progress.advance(task_2)

        # Add every vendors to a set.
        # As the set does not allow duplicate members, the resultant set will be unique.
        vendors = set(boards["vendor"] for boards in sorted_boards)

        # Format the output including the _metadata with number of unique vendors and total number of boards
        output = {
            "boards": sorted_boards,
            "_metadata": {
                "total_vendors": len(vendors),
                "total_boards": len(sorted_boards),
            },
        }
        print("\n [bold blue]The combined output: [/bold blue]")

        # Since 'print' function from 'rich' is used, the output will be pretty printed
        print(output)

        # Save the output to the merged folder.
        # TODO - User chosen output folder
        task_3 = progress.add_task(description="Saving the Result...", total=None)

        # Custom path and file name for the output JSON file
        merged_path = "merged"
        # Current timestamp is added for information and uniqueness
        file_name = "boards_data_merged-" + str(int(time.time())) + ".json"

        # Save the output to the file.
        with open(merged_path + "/" + file_name, "w") as fp:
            # 'indent' argument ensures that the file saved in a readable manner
            json.dump(output, fp, indent=4)
        time.sleep(1)
        progress.advance(task_3)

        # Announce where the file is saved
        print(
            f"\n The output is saved as [bold green]'{file_name}'[/bold green] in the [bold green]'{merged_path}'[/bold green] folder"
        )


if __name__ == "__main__":
    app()
