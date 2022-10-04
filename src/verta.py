#!/usr/bin/env python3
import functools
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment
from elftools.elf.constants import SH_FLAGS
import mmap
from image import Image
import tempfile
import argparse

parser = argparse.ArgumentParser(description='verta: decorated hexdump.')
parser.add_argument('--elf', action='append', nargs='+', required=True, help='input, ELF files')
parser.add_argument('--hex', action='append', nargs='+', required=True, help='input, HEX file')
parser.add_argument('--output', default='-',
                    help='output, file to write output to, default -')

parser.add_argument('--short', '-s', action='store_true', help='short output')
parser.add_argument('--verbose', '-v', action='store_true', help='verbose flag')

args = parser.parse_args()

# Number of elf files:
elf_number = 0
hex_number = 0

input_elf_files = []
for lst in args.elf:
    for e in lst:
        # print(e)
        input_elf_files.append(e)
        elf_number += 1

for lst in args.hex:
    for h in lst:
        # print(e)
        hex_number += 1

# Sanity check:
if elf_number <= 0:
    parser.print_help()
    sys.exit(0)

if hex_number > 1 or hex_number <= 0:
    parser.print_help()
    sys.exit(0)

input_hex = args.hex[0][0]

def align_up(num, align):
    assert (align & (align - 1) == 0) and align != 0
    return (num + (align - 1)) & ~(align - 1)


# Temp directory:
with tempfile.TemporaryDirectory() as temp_dir:
    temp_file = temp_dir + "/" + "input.bin"

    i = Image()
    i.load(input_hex)
    elf_base_address = i.get_base_address()
    elf_max_address = i.get_max_address()
    # temp_file = TEMPDIR + "/" + "input.bin"
    i.save(temp_file)

    if args.verbose:
        print(f"Loaded file {input_hex} with base address {hex(elf_base_address)} and max address \
              {hex(elf_max_address)}")

    section_infos = []
    segment_infos = []

    with open(temp_file, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)

        for input_elf in input_elf_files:
            segments_of_interrest = []
            with open(input_elf, 'rb') as elffile:
                for segment in ELFFile(elffile).iter_segments():
                    if segment.header.p_type == "PT_LOAD":
                        segment_infos.append(
                            {
                                "p_offset": segment.header['p_offset'],
                                "p_vaddr": segment.header['p_vaddr'],
                                "p_filesz": segment.header['p_filesz'],
                                "p_memsz": segment.header['p_memsz'],
                            }
                        )
                        segments_of_interrest.append(segment)

                # wanted_sections = ["SHT_PROGBITS", "SHT_NOBITS"]
                wanted_sections = ["SHT_PROGBITS"]

                for section in ELFFile(elffile).iter_sections():
                    if section.header['sh_type'] in wanted_sections:
                        o = section.header['sh_offset']
                        count = 0
                        for segment in segment_infos:
                            if segment['p_offset'] <= o < (segment['p_offset'] + segment['p_filesz']):
                                section_address = \
                                    align_up(segment['p_vaddr'] + (o - segment['p_offset']), section["sh_addralign"])
                                from_base_offset = section_address - elf_base_address
                                found_offset = mm.find(section.data(), from_base_offset)
                                data_found = (found_offset != -1)
                                if not data_found:
                                    found_offset = mm.find(section.data(), 0)
                                    data_found = (found_offset != -1)

                                section_infos.append(
                                    {
                                        "name": section.name,
                                        "address": section_address,
                                        "segment_id": count,
                                        "found_offset": found_offset,
                                        "data_found": data_found,
                                        "output": True
                                    }
                                )
                            count += 1

    original_stdout = sys.stdout
    if args.output != "-":
        output = open(args.output, 'w')
        sys.stdout = output

    # Write a hexdump of the bin file:
    with open(temp_file, "r+b") as f:
        it = iter(functools.partial(f.read, 16), '')

        for i, b in enumerate(it):
            start_address: int = elf_base_address + (16 * i)

            # Check if current range is in the list of addresses:
            range_start = start_address
            range_end = start_address + 16

            decoration = ""
            for si in section_infos:
                if range_start <= si['address'] < range_end:
                    decoration = f" Section: {si['name']} ({hex(si['address'])})"

            if start_address > elf_max_address:
                break
            if args.short:
                if decoration:
                    print(f'{start_address:07x} {b.hex(" ", 2)}{decoration}')
            else:
                print(f'{start_address:07x} {b.hex(" ", 2)}{decoration}')
    sys.stdout = original_stdout
    if args.output != "-":
        output.close()
sys.exit(0)
