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
    print("Usage: script <elf> <hex>")
    #print("You must provide this script with an elf binary file you want to examine")
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
    #print(mm.find(b'\x00\x09\x03\x03'))

    #with open(sys.argv[2], "r") as f:
    #    mm = mmap.mmap(f.fileno(), 0)
    #    print(mm.find('\x00\x09\x03\x03'))

    # TODO: output a hexdump of the bin file decorated with sections that match the offsets in the bin file.
    segments_of_interrest = []
    with open(sys.argv[1], 'rb') as elffile:
        for segment in ELFFile(elffile).iter_segments():
            if segment.header.p_type == "PT_LOAD":
                #print(segment.header)
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
                #print(f"{section.name}")
                #print(f"{section.header}")
                o = section.header['sh_offset']
                count = 0
                for segment in segment_infos:
                    if segment['p_offset'] <= o < (segment['p_offset'] + segment['p_filesz']):
                        #print(f"{section.header}")
                        #print(f"{section.name} => {count} => {hex(segment['p_vaddr'])}")

                        section_address = \
                            align_up(segment['p_vaddr'] + (o - segment['p_offset']), section["sh_addralign"])
                        #print(f"section_address={hex(section_address)}, sh_addr={hex(section.header['sh_addr'])}")
                        #if section.header['sh_flags'] & SH_FLAGS.SHF_WRITE:
                        #    print("SHF_WRITE")
                        #if section.header['sh_flags'] & SH_FLAGS.SHF_ALLOC:
                        #    print("SHF_ALLOC")

                        from_base_offset = section_address - elf_base_address
                        #print(f"from_base_offset={hex(from_base_offset)}")

                        found_offset = mm.find(section.data(), from_base_offset)
                        data_found = (found_offset != -1)
                        #if data_found:
                        #    print(f"Data found at offset: {hex(found_offset)}")
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

# 00cd6c0 4241 3231 3537 4534 0a42 303a 3030 3030

# Write a hexdump of the bin file:

with open(temp_file, "r+b") as f:
    it = iter(functools.partial(f.read, 16), '')

    for i, b in enumerate(it):
        a = elf_base_address + (16*i)
        if a > elf_max_address:
            break
        print(f'{a:07x} {b.hex(" ", 2)}')

sys.exit(0)


