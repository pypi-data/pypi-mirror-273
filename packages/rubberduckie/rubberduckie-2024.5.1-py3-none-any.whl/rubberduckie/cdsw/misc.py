import subprocess


def clean_cdsw_project_trash():
    """Clean trash in CDSW project

    Author:
        Justin Trinh @ 2024-05
    """

    # Retrieve size of Trash folder
    subprocess_trash = subprocess.run(
        ["du", "-hs", "/home/cdsw/.local/share/Trash"], capture_output=True, text=True
    )
    print("Size and location of trash in your project:")
    print(subprocess_trash.stdout)

    # Delete Trash Folder
    response = input("Would like like to clean trash (Y/N)?")
    if response.lower() in ["y", "yes", "yep"]:
        print("Cleaning trash...")
        subprocess.run(
            ["rm", "-rf", "/home/cdsw/.local/share/Trash"],
            capture_output=True,
            text=True,
        )
        print("Done!")
