import argparse
from splitpdf_pro import __version__
import PyPDF2

def split_pdf(input_file, page_ranges):
    """Splits a PDF into multiple files based on the given page ranges.

    Args:
        input_file (str): Path to the input PDF file.
        page_ranges (str): Comma-separated or space-separated string representing page ranges or single pages.

    Returns:
        None
    """
    if ',' in page_ranges:
        page_ranges = page_ranges.split(',')
    elif ' ' in page_ranges:
        page_ranges = page_ranges.split(' ')

    with open(input_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Validate page ranges and handle potential errors
        for page_range in page_ranges:
            try:
                if '-' in page_range:
                    start, end = map(int, page_range.split('-'))
                    if start < 1 or start > end or end > num_pages:
                        raise ValueError(f"Invalid page range: {page_range}")
                else:
                    page_num = int(page_range)
                    if page_num < 1 or page_num > num_pages:
                        raise ValueError(f"Invalid page number: {page_num}")
            except ValueError as e:
                print(f"Error: {e}")
                continue  # Skip invalid ranges and continue processing others

        # Create output files for valid ranges/pages
        current_page = 1
        for page_range in page_ranges:
            if '-' in page_range:
                start, end = map(int, page_range.split('-'))
                pdf_writer = PyPDF2.PdfWriter()
                for page in range(start - 1, end):  # Account for 0-based indexing
                    pdf_writer.add_page(pdf_reader.pages[page])
                output_filename = f"{input_file.replace('.pdf', '')}_{start}-{end}.pdf"
                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)
                    print(f"Created output file: {output_filename}")
            else:
                page_num = int(page_range)
                pdf_writer = PyPDF2.PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num -1])
                output_filename = f"{input_file.replace('.pdf', '')}_{page_num}.pdf"
                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)
                    print(f"Created output file: {output_filename}")
                current_page = page_num + 1  # Update current page for clarity with single pages



package_name = "splitpdf-pro"

example_uses = '''example:
   splitpdf-pro file.pdf
   splitpdf-pro file.pdf -r 2,4-6,8
   splitpdf file.pdf
   splitpdf file.pdf -r 2,4-6,8'''

def main(argv = None):
    parser = argparse.ArgumentParser(prog=package_name, description="Split pdf", epilog=example_uses, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('filename', type=str, help='Path to the input PDF file')
    parser.add_argument('-r', '--ranges', type=str, help="Give Comma-separated range numbers or single numbers")

    parser.add_argument('-v',"--version",
                            action="version",
                            version=__version__,
                            help="check version of deb")

    args = parser.parse_args(argv)

    if args.filename:
        if args.ranges:
            split_pdf(args.filename, args.ranges)
        else:
            ranges = input('Enter Comma-separated or space-separated range numbers or single numbers : ')
            split_pdf(args.filename, ranges)
    else:
        parser.print_help()

if __name__ == "__main__":
    raise SystemExit(main())