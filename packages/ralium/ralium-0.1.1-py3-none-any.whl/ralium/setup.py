from ralium.errors import DisableWarnings
import PyInstaller.__main__
import sys
import os

HTML_FILE_EXTENSIONS = [".htm", ".html"]

def _exe_str_error(name, var):
    return TypeError(f"Expected executable {name} to be of type 'str', instead got '{type(var)}'")

def _add_data_arg(src, dst):
    return f'--add-data={src}{os.pathsep}{dst}'

def collect_webfolder(webfolder):
    """
    Collects all necessary files from a Ralium Web Folder used within the executable main Python file.

    :param webfolder: The path to the project folder.
    
    :returns: A dictionary where the keys contain the absolute paths and the values represent the relative paths.
    """

    webfiles = {}
    webfolder = os.path.abspath(webfolder)
    webroutes = os.path.join(webfolder, "routes")
    cssfolder = os.path.join(webfolder, "styles")
    imgfolder = os.path.join(webfolder, "images")
    webfolder_name = os.path.basename(webfolder)
    
    if os.path.exists(webroutes):
        for root, _, files in os.walk(webroutes):
            dest = os.path.normpath(f"{webfolder_name}\\{root.removeprefix(webfolder)}")
            webfiles.update({os.path.join(root, file): os.path.join(dest, file) for file in files if os.path.splitext(file)[-1] in HTML_FILE_EXTENSIONS})
    
    if os.path.exists(cssfolder):
        for root, _, files in os.walk(cssfolder):
            dest = os.path.normpath(f"{webfolder_name}\\{root.removeprefix(webfolder)}")
            webfiles.update({os.path.join(root, file): os.path.join(dest, file) for file in files if os.path.splitext(file)[-1] == ".css"})
    
    if os.path.exists(imgfolder):
        for root, _, files in os.walk(imgfolder):
            dest = os.path.normpath(f"{webfolder_name}\\{root.removeprefix(webfolder)}")
            webfiles.update({os.path.join(root, file): os.path.join(dest, file) for file in files})
    
    return webfiles

def setup(
    pyfile,
    name = None,
    icon = None,
    onefile = True,
    warnings = False,
    noconsole = True,
    webfolder = None,
    *pyi_args
):
    """
    Compiles a Ralium project using PyInstaller.

    :param pyfile: Python file to compile.
    :param name: Display name for the executable.
    :param icon: Display icon for the executable.
    :param onefile: Bundles the executable as a standalone file.
    :param warnings: Calls the `DisableWarnings` to prevent warnings.
    :param noconsole: Prevents a console from being displayed.
    :param webfolder: Directory of the project.
    :param pyi_args: Extra parameters for PyInstaller to use.

    :raises TypeError: If the name or icon is not a `str` or `None`.
    :raises RuntimeError: If this function is called within an already compiled executable file.
    :raises FileNotFoundError: If a certain file path doesn't exist.
    """

    if getattr(sys, "frozen", False):
        raise RuntimeError("Ralium setup cannot be ran from an executable file.")
    
    if not os.path.exists(pyfile):
        raise FileNotFoundError(f"Failed to find python file '{pyfile}'")

    args = [pyfile, *pyi_args]

    if name is not None:
        if not isinstance(name, str):
            raise _exe_str_error("name", name)
        
        args.append(f"--name={name}")
    
    if icon is not None:
        if not isinstance(icon, str):
            raise _exe_str_error("icon", icon)

        if not os.path.exists(icon):
            raise FileNotFoundError(f"Failed to find icon file with path: '{icon}'")
        
        args.append(f"--icon={icon}")
    
    if onefile:
        args.append(f"--onefile")
    
    if not warnings:
        DisableWarnings()
    
    if noconsole:
        args.append(f"--noconsole")
    
    if webfolder:
        for src, dst in collect_webfolder(webfolder).items():
            args.append(_add_data_arg(src, dst))

    PyInstaller.__main__.run(args)