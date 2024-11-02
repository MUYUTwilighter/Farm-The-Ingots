from json import load
from os import makedirs, listdir, walk
from os.path import isdir, join, relpath, exists
from shutil import rmtree, copytree, copy2
import re
import zipfile

properties = {}
with open("properties.json") as f:
    properties = load(f)
    f.close()

def validate_path(path: str) -> None:
    if (not isdir(path)):
        makedirs(path)

def clear_cache() -> None:
    """
    Clears the cache directory by removing it and recreating it.

    :return: None
    """
    print("Clearing cache")
    CACHE_PATH = properties["path"]["cache"]
    validate_path(CACHE_PATH)
    rmtree(CACHE_PATH)
    makedirs(CACHE_PATH)

def copy_content(src: str, dst: str) -> None:
    """
    Copies all contents from the source directory to the destination directory.

    If an item in the source is a directory, it will recursively copy all contents,
    preserving the directory structure. If an item is a file, it will copy the file 
    directly to the destination.

    :param src: The source directory path.
    :param dst: The destination directory path.
    :return: None
    """
    validate_path(dst)
    for item in listdir(src):
        s = join(src, item)
        d = join(dst, item)
        if isdir(s):
            if exists(d):
                rmtree(d)
            copytree(s, d)
        else:
            copy2(s, d)

def find_placeholders(content: str) -> list[str]:
    """
    Finds all placeholders in the given content in the format ${key}.
    
    :param content: The content to search in.
    :return: A list of all found placeholder keys.
    """
    return re.findall(r"\$\{([a-zA-Z0-9_.]+)\}", content)

def get_placeholder_value(key: list[str], **kwargs: list[any] | dict[any, any]) -> any:
    """
    Try to get the value from either the given keyword arguments or the loaded properties.
    
    :param key: A list of strings that should be used to traverse a dictionary.
    :param kwargs: The keyword arguments to search first.
    :return: The value found at the given key, or raise KeyError if not found.
    :raises KeyError: If the key is not found in either kwargs or properties.
    """
    try:
        tmp = kwargs
        for sep in key:
            tmp = tmp[sep]
        return tmp
    except KeyError:
        pass
    try:
        tmp = properties
        for sep in key:
            tmp = tmp[sep]
        return tmp
    except KeyError:
        print(f"Placeholder {key} not found in neither properties nor kwargs")
        raise KeyError(key)

def get_placeholders_values(keys: list[str], **kwargs: list[any] | dict[any, any]) -> dict[str, any]:
    """
    Takes a list of keys in the format "a.b.c" and returns a dict with the corresponding values from either the properties or the kwargs.
    If a key is not found in either the properties or the kwargs, it is skipped.
    """
    output = {}
    for key in keys:
        try:
            output[key] = get_placeholder_value(key.split("."), **properties)
        except KeyError:
            continue
    for key in keys:
        try:
            output[key] = get_placeholder_value(key.split("."), **kwargs)
        except KeyError:
            continue
    return output
    

def map_placeholders(content: str, mapping: dict[str, any]) -> str:
    """
    Replaces placeholders in the given content with corresponding values from the mapping.

    Args:
        content (str): The content containing placeholders to be replaced.
        mapping (dict[str, any]): A dictionary where keys represent placeholders (without ${})
            and values are the replacements for those placeholders.

    Returns:
        str: The content with placeholders replaced by their corresponding values from the mapping.
    """
    for key in mapping.keys():
        content = content.replace("${" + key + "}", str(mapping[key]))
    return content

def handle_placeholders(content: str, **kwargs: list[any] | dict[any, any]) -> str:
    """
    Replaces placeholders in the given content using the given kwargs (higher priority)
    or properties.

    Args:
        content (str): The content to replace placeholders in.
        **kwargs (list[any] | dict[any, any]): The values to replace placeholders with.

    Returns:
        str: The processed content.
    """
    return map_placeholders(content, get_placeholders_values(find_placeholders(content), **kwargs))

def fhandle_placeholders(file_path: str, **kwargs: list[any] | dict[any, any]):
    """
    Reads a file at the given path, handles placeholders in the content
    using the given kwargs (higher priority) or properties,
    and writes it back to the file.

    Args:
        file_path (str): The path to the file to read and write.
        **kwargs (list[any] | dict[any, any]): The values to replace placeholders with.
    """
    print("Handling placeholders in " + file_path)
    content = ""
    with open(file_path) as f:
        content = f.read()
        f.close()
    content = handle_placeholders(content, **kwargs)
    with open(file_path, "w") as f:
        f.write(content)
        f.close()

def archive_cache(archive_name: str) -> None:
    """
    Archives the cache directory into a zip file with the given name.

    Args:
        archive_name (str): The name of the archive to create.

    Returns:
        None
    """
    print("Archiving cache to " + archive_name + ".zip")
    CACHE_PATH = properties["path"]["cache"]
    BUILD_PATH = properties["path"]["build"]
    validate_path(CACHE_PATH)
    validate_path(BUILD_PATH)
    with zipfile.ZipFile(join(BUILD_PATH, archive_name + ".zip"), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in walk(CACHE_PATH):
            for file in files:
                zipf.write(join(root, file), join(relpath(root, CACHE_PATH), file))
        zipf.close()

def copy_content2cache(src: str) -> None:
    """
    Copies the contents from the given source directory to the cache directory.

    Args:
        src (str): The source directory path.

    Returns:
        None
    """
    print("Copying " + src + " to cache")
    CACHE_PATH = properties["path"]["cache"]
    validate_path(CACHE_PATH)
    copy_content(src, CACHE_PATH)