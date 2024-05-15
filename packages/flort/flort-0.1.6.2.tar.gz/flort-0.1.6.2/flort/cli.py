import os
import argparse
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_content(file_path):
    """Cleans up the content of a file by removing unnecessary whitespace."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(cleaned_lines)

def generate_tree(directories, extensions=None):
    """Generates a tree structure for multiple directories."""
    tree_structure = ''
    for directory in directories:
        directory = str(directory)  # Convert directory to string
        for root, dirs, files in os.walk(directory):
            if extensions:
                dirs[:] = [d for d in dirs if any(Path(root) / d / f for f in os.listdir(Path(root) / d) if Path(f).suffix in extensions)]
                included_files = [f for f in files if Path(f).suffix in extensions]
            else:
                included_files = files
            
            level = root.replace(directory, '').count(os.sep)
            indent = '|   ' * level + '|-- '
            sub_indent = '|   ' * (level + 1) + '|-- '

            if included_files or dirs:
                tree_structure += f"{indent}{os.path.basename(root)}/\n"
                for file in included_files:
                    tree_structure += f"{sub_indent}{file}\n"
    return tree_structure

def list_files(directories, compress=False, extensions=None):
    """Lists files in multiple directories."""
    try:
        files_info = []
        num_files = 0
        for directory in directories:
            directory_path = Path(directory)
            if not directory_path.is_dir():
                logging.error(f"The path {directory} is not a valid directory.")
                continue

            #logging.info(f"Processing directory: {directory_path}")

            for file_path in directory_path.rglob('*'):
                if file_path.is_file() and '.git' not in file_path.parts:
                    if extensions is None or file_path.suffix.lower() in extensions:
                        num_files += 1
                        file_info = [f"Path: {file_path}", f"File: {file_path.name}", "-------"]

                        try:
                            if compress:
                                compressed_content = clean_content(file_path)
                                file_info.append(compressed_content)
                            else:
                                with open(file_path, 'r') as f:
                                    file_info.append(f.read())
                        except Exception as e:
                            logging.error(f"Error reading file {file_path}: {e}")
                        
                        files_info.append('\n'.join(file_info))

        logging.info(f"Number of eligible files processed: {num_files}")
        return '\n'.join(files_info)
    except Exception as e:
        logging.error(f"Error processing directories: {e}")
        return ""
    
def write_file(file_path, data):
    """Writes data to the specified file."""
    with open(file_path, 'w') as file:
        file.write(data)
    logging.info(f"Output written to file: {file_path}")

def print_configuration(directories, extensions):
    """Prints the directories and extensions being processed."""
    logging.info(f"Directories being processed: {', '.join(directories)}")
    logging.info(f"File extensions being processed: {', '.join(extensions)}")

def main():
    """Main function to parse arguments and execute operations."""
    parser = argparse.ArgumentParser(description="flort: List and optionally compress files in directories.", prog='flort')
    parser.add_argument('directories', metavar='DIRECTORY', type=str, nargs='+', help='Directories to list files from.')
    parser.add_argument('--compress', default=False, action='store_true', help='Compress the listed files by removing whitespace.')
    parser.add_argument('--output', type=str, default="stdio", help='Output file path. Defaults to stdout if not specified.')
    parser.add_argument('--no-tree', action='store_true', help='Do not print the tree at the beginning.')
    args, unknown_args = parser.parse_known_args()

    # Treat unknown args as extensions that start with '--'
    extensions = [f".{ext.lstrip('-')}" for ext in unknown_args if ext.startswith('--')]

    # Print configuration
    print_configuration(args.directories, extensions)

    output_content = []
    if not args.no_tree:
        output_content.append(generate_tree(args.directories, extensions=extensions))

    output_content.append(list_files(args.directories, compress=args.compress, extensions=extensions))

    if args.output != "stdio":
        write_file(args.output, "\n".join(output_content))
    else:
        print("\n".join(output_content))

if __name__ == "__main__":
    main()
