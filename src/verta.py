#!/usr/bin/env python3
import functools
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment
from elftools.elf.constants import SH_FLAGS
import mmap
from image import Image

input_elf = sys.argv[1]
input_hex = sys.argv[2]

if len(sys.argv) < 3:
    print("Usage: script <elf file 1> .. <elf file n> <hex>")
    sys.exit(1)

# Temp directory:
TEMPDIR = "./temp"

i = Image()
i.load(input_hex)
elf_base_address = i.get_base_address()
elf_max_address = i.get_max_address()
temp_file = TEMPDIR + "/" + "input.bin"
i.save(temp_file)

print(f"Loaded file {input_hex} with base address {hex(elf_base_address)} and max address {hex(elf_max_address)}")

section_infos = []
segment_infos = []

def align_up(num, align):
    assert (align & (align - 1) == 0) and align != 0
    return (num + (align - 1)) & ~(align - 1)

with open(temp_file, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    segments_of_interrest = []
    with open(sys.argv[1], 'rb') as elffile:
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

        #wanted_sections = ["SHT_PROGBITS", "SHT_NOBITS"]
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

# Write a hexdump of the bin file:
with open(temp_file, "r+b") as f:
    it = iter(functools.partial(f.read, 16), '')

    for i, b in enumerate(it):
        start_address: int = elf_base_address + (16*i)

        # Check if current range is in the list of addresses:
        range_start = start_address
        range_end = start_address + 16

        decoration = ""
        for si in section_infos:
            if range_start <= si['address'] < range_end:
                decoration = f" Section: {si['name']} ({hex(si['address'])})"

        if start_address > elf_max_address:
            break
        print(f'{start_address:07x} {b.hex(" ", 2)}{decoration}')

sys.exit(0)


