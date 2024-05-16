import pymupdf
import argparse


def unmark(infilename, outfilename, garbage):
    with pymupdf.open(infilename, filetype='pdf') as doc:
        doc.set_metadata({})
        doc.del_xml_metadata()
        for page in doc:
            content_xrefs = page.get_contents()
            page.set_contents(content_xrefs[0])
        doc.save(outfilename, garbage=garbage)

def main():
    parser = argparse.ArgumentParser(
        description='Utility to remove PII watermarks from pdfs downloaded from Move USP/ESALQ.'
    )
    parser.add_argument('input', help='input filename')
    parser.add_argument(
        '-o', '--output', 
        default='unmarked.pdf', 
        help='output filename (default: "unmarked.pdf")',
    )
    parser.add_argument(
        '-g', '--garbage', 
        default=1, type=int, 
        help='level of garbage collection (default: 1)',
    )
    args = parser.parse_args()
    unmark(args.input, args.output, args.garbage)

if __name__ == '__main__':
    main()
