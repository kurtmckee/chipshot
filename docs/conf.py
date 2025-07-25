import datetime
import pathlib
import tomllib

# General configuration
# ---------------------

# The suffix of source filenames.
source_suffix = ".rst"

# The main toctree document.
master_doc = "index"

# General information about the project.
project = "Chipshot"
copyright = f"2022-{datetime.datetime.now().strftime('%Y')} Kurt McKee"

# Extract the project version.
pyproject_ = pathlib.Path(__file__).parent.parent / "pyproject.toml"
info_ = tomllib.loads(pyproject_.read_text())
version = release = info_["project"]["version"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# HTML theme configuration
# ------------------------

html_theme = "alabaster"
html_static_path = [
    "_static",
]
html_theme_options = {
    "logo": "logo.png",
    "logo_name": "Chipshot",
    # Link to GitHub
    "github_user": "kurtmckee",
    "github_repo": "chipshot",
    "github_button": True,
    "github_type": "star",
    "github_count": False,
    # Don't show "Powered by" text.
    "show_powered_by": False,
}

# Don't copy source .rst files into the built documentation.
html_copy_source = False
