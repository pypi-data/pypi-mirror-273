import argparse
import os
from pathlib import Path

def list_files(base_path, recurse, name_filters=None, filetype=None):
    ignored_dirs = {'.git', '__pycache__'}
    file_dict = {}

    if recurse:
        walker = os.walk(base_path)
    else:
        walker = [(base_path, next(os.walk(base_path))[1], next(os.walk(base_path))[2])]

    for root, dirs, files in walker:
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        print(f"Processing directory: {root}")

        depth = root[len(base_path):].count(os.sep)
        relevant_files = [
            f for f in files if (
                (name_filters is None or any(f.startswith(n) for n in name_filters.split(' | '))) and
                (filetype is None or f.endswith(filetype))
            )
        ]

        if relevant_files:
            header = '#' * (depth + 2)  # Parent directory is #, first level is ##
            file_dict[root] = {
                "header": header,
                "files": relevant_files
            }
            print(f"Adding {len(relevant_files)} files under: {root}")

    return file_dict

def write_markdown(file_dict, output_file, base_path):
    base_dir_name = os.path.basename(base_path.rstrip('/'))
    with open(output_file, 'w', encoding='utf-8') as md_file:
        print(f"Writing to {output_file}")
        for path, data in sorted(file_dict.items(), key=lambda x: x[0]):
            relative_path = os.path.relpath(path, base_path)
            if relative_path == '.':
                relative_path = base_dir_name
            md_file.write(f"{data['header']} {relative_path}\n")
            for filename in data['files']:
                file_ext = Path(filename).suffix.lstrip('.')
                if not file_ext:
                    file_ext = 'text'
                md_file.write(f"{data['header']}# {filename}\n")
                file_path = os.path.join(path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    md_file.write(f"```{file_ext}\n{content}\n```\n")

def main():
    parser = argparse.ArgumentParser(description="Generate a Markdown file from directory contents.")
    parser.add_argument("path", help="Path to the directory")
    parser.add_argument("-r", "--recurse", action='store_true', help="Recurse into subdirectories")
    parser.add_argument("-n", "--name", help="Filter files by name, separated by ' | '", type=str)
    parser.add_argument("-t", "--type", help="Filter files by file type")
    parser.add_argument("-o", "--output", help="Output markdown file name")

    args = parser.parse_args()

    file_dict = list_files(args.path, args.recurse, name_filters=args.name, filetype=args.type)
    output_filename = args.output if args.output else f"{os.path.basename(args.path)}-{'-'.join(args.name.split(' | ') if args.name else ['marked']).replace(' ', '-')}.md"

    write_markdown(file_dict, output_filename, args.path)

if __name__ == "__main__":
    main()
