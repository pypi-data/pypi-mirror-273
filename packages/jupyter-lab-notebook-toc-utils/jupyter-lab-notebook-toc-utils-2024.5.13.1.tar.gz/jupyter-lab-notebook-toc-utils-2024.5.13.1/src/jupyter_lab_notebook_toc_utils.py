from IPython.display import display, Markdown
from nbconvert import MarkdownExporter
import nbformat
import os
import urllib.parse
from IPython import get_ipython

def generate_toc(
        nb_path: str = None, 
        title: str = "Table of Contents", 
        depth: int = 3,
        make_hyperlinks: bool = True,
        bullet_char: str = "",
        add_numbering: bool = False,
        bold_numbering: bool = True,
        bold_header_depth: int = 1
    
    ) -> str:
    """
    Build a table of contents for a Jupyter notebook.

    Parameters
    ----------
    nb_path : str, optional
        The path to the Jupyter notebook file.
    title : str, optional
        The title of the table of contents.
    depth : int, optional
        The maximum depth of headings to include in the table of contents.
    make_hyperlinks : bool, optional
        Whether to make the table of contents entries hyperlinks.
    bullet_char : str, optional
        The character to use for the bullets in the TOC
    add_numbering: bool, optional
        Whether or not to add numbering to the headers in the TOC
    bold_numbering: bool, optional
        Whether or not to bold the numbering if/when it is added
    bold_header_depth: int, optional
        The depth to which headers should be bolded.
    
    Returns
    -------
    str
        The table of contents as a Markdown-formatted string.

    Raises
    ------
    FileNotFoundError
        If the specified notebook path does not exist.
    """
    
    # Check if we are running inside a notebook
    running_in_notebook = False
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            running_in_notebook = True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            running_in_notebook = False  # Terminal running IPython
    except NameError:
        pass

    # If we are in a notebook, and no path was provided, determine the path
    if running_in_notebook and not nb_path:
        import ipynbname
        nb_name = ipynbname.name() + ".ipynb"
        nb_path = nb_name # Notebook cell running this should be able to resolve relative path
    
    # Load the notebook into an object
    if not os.path.exists(nb_path):
        raise FileNotFoundError(f"The path '{nb_path}' does not exist.")
    nb = nbformat.read(nb_path, nbformat.NO_CONVERT)

    # Iterate through the markdown cells to generate the table of contents
    levels = []
    previous_level = None
    toc = [f"**{title}**"]
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            for line in cell.source.split("\n"):
                if line.startswith("#"):

                    # Count how many consecutive hash (#) characters appear at the start of the string
                    # to determine the level of the section
                    level_prefix = line.split()[0]
                    level = len(level_prefix)

                    # Ignore cells for levels that are too deep
                    if level > depth:
                        continue
                    
                    # Keep track of how many elements we have seen at each level
                    if add_numbering:
                        # If we are moving up a level, rather than going deeper, do the cleanup
                        if previous_level and previous_level > level:
                            levels = levels[:level]
                        # If it's the first time at the level, add an entry to the list
                        if len(levels) < level:
                            levels.append(1)
                        # If we have already been to this level, increment it
                        else:
                            levels[level - 1] += 1                      
                        


                    
                    # Remove the leading # characters to retrieve the text for the header
                    text = line.lstrip(level_prefix)
                    text = text.strip()

                    # We cannot use a markdown list to represent the TOC because it has
                    # restrictions for how the nested elements appear; they sub-levels must
                    # appear incrementally and we cannot "skip ahead" or "skip levels"
                    # As such, we will hardcode spaces instead and use <br/>\n to separate the lines.
                    leading_spaces = "&nbsp;" * 4 * (level)

                    if bullet_char is not None:
                        bullet_text = f"{bullet_char} "
                    else:
                        bullet_text = bullet_char
                    
                    # If the user wants to add numbering, add it
                    numbering_prefix = ""
                    if add_numbering:
                        numbering_prefix = ".".join([str(level) for level in levels]) + "."
                        if bold_numbering:
                            numbering_prefix = f"**{numbering_prefix}**"
                        numbering_prefix += " "
                    
                    # If the user wants to bold headers, bold them
                    if bold_header_depth >= level:
                        formatted_text = f"**{text}**"
                    else:
                        formatted_text = text
                    
                    # Create the TOC entry for the markdown cell
                    if make_hyperlinks:
                        
                        # For markdown based hyperlinks there are certain rules we need to abide by
                        # and we cannot simply url-encode the special characters
                        # Jupyter lab has it's own logic as well which can occationally break things
                        # since some of the link/anchor behavior is handled through JS rather than raw
                        # browser based functionality.
                        
                        # Fist we replace spaces with minus characters
                        link_text = text.replace(" ", "-")

                        # Next we remove any escape characters
                        link_text = link_text.replace("\\", "")

                        # Then we url-encode any remaining special characters
                        url_escape_chars = "^{}[]()$"
                        url_escape_codes = {char: urllib.parse.quote_plus(char) for char in url_escape_chars}
                        for char, escape in url_escape_codes.items():
                            link_text = link_text.replace(char, escape)
                        
                        toc_entry = f"{leading_spaces}{bullet_text}[{numbering_prefix}{formatted_text}](#{link_text})"
                    else:
                        toc_entry = f"{leading_spaces}{bullet_text}{numbering_prefix}{formatted_text}"
                    
                    # Update our pointer if necessary
                    if add_numbering:
                        previous_level = level
                    
                    toc.append(toc_entry)

    return ("<br/>" + os.linesep).join(toc)
    
def display_toc(toc_str):
    display(Markdown(toc_str))