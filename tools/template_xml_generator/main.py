import logging
import yaml
import argparse
import jinja2
import sys
from pathlib import Path

logger = logging.getLogger('default_logger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)

parser = argparse.ArgumentParser(description="SLCP generator script")
parser.add_argument('--extension-root'  , required=True, help='Path to your extension directory)')
parser.add_argument('--output-directory', required=False, help='Path to the directory where the output will be generated)')
args = parser.parse_args()

def get_files_with_extension(rootpath: Path, extenion: str):
    found_files = []
    for path_object in rootpath.rglob('*'):
        if path_object.is_file():
            if path_object.suffix == extenion:
                logger.info(f"Found {path_object}")
                found_files.append(path_object)

    return found_files

def find_slcp_files(rootpath: Path):
    return get_files_with_extension(rootpath, ".slcp")

def process_slcps(slcps):
    processed_slcp = {}
    for slcp in slcps:
        with open(slcp, 'r') as file:
            content = yaml.safe_load(file)
            processed_slcp[slcp] = content
    return processed_slcp

def render_xml(extension_directory_name, output_directory, slcp_raw_content):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)
    template = templateEnv.get_template("template.xml.jinja")

    prepared_xml_fields = []

    for slcp, content in slcp_raw_content.items():
        entry = {}

        slcp_path_str = str(slcp)
        
        extension_relative_slcp_path = slcp_path_str[slcp_path_str.find(extension_directory_name):]

        entry["label"] = content["label"]
        entry["description"] = content["description"]
        entry["quality"]  = content["quality"].upper()
        entry["readme"]   = content["readme"][0]["path"]
        entry["category"] = content["category"]
        entry["solution_reference"] = str(extension_relative_slcp_path).replace('/', '.').replace('\\', '.')
        entry["project_file_paths"] = str(extension_relative_slcp_path)
        entry["filter"] = ""

        filters = []
        for filter in content["filter"]:
            name   = filter["name"].replace(' ', '\\ ')
            value  = filter["value"][0].replace(' ', '\\ ')
            filters.append( '|'.join([name, value]))
        
        entry["filter"] = ' '.join(filters)

        prepared_xml_fields.append(entry)

    outputText = template.render(slcp_list = prepared_xml_fields)

    output_xml_full_path = output_directory.joinpath(f"templates.xml")

    with open(output_xml_full_path, 'w') as f:
        f.write(outputText)
        logger.info(f"templates.xml generated successfully!")

def main(root_path, output_directry_path):
    slcps = find_slcp_files(root_path)

    slcp_raw_content = process_slcps(slcps)

    extension_directory_name = root_path.name
    render_xml(extension_directory_name, output_directry_path, slcp_raw_content)

if __name__ == "__main__":
    
    extension_root_path  = Path(args.extension_root)
    output_directry_path = Path().cwd()

    if args.output_directory:
        output_directry_path = Path(args.output_directory)
        if output_directry_path.is_dir() is False:
            logger.error(f"{args.extension_root} does not exists, creating!")
            Path.mkdir(output_directry_path)
    
    if extension_root_path.is_dir() is False:
        logger.error(f"{args.extension_root} does not exists!")
        sys.exit()

    main(extension_root_path, output_directry_path)