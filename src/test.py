#!/usr/bin/env python3
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment
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
ba = i.get_base_address()
temp_file = TEMPDIR + "/" + "input.bin"
i.save(temp_file)

print(f"Loaded file {input_hex} with base address {hex(ba)}")

with open(temp_file, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    #print(mm.find(b'\x00\x09\x03\x03'))

    #with open(sys.argv[2], "r") as f:
    #    mm = mmap.mmap(f.fileno(), 0)
    #    print(mm.find('\x00\x09\x03\x03'))

    segments_of_interrest = []
    with open(sys.argv[1], 'rb') as elffile:
        for segment in ELFFile(elffile).iter_segments():
            if segment.header.p_type == "PT_LOAD":
                #print(segment.header)
                segments_of_interrest.append(segment)

        #wanted_sections = ["SHT_PROGBITS", "SHT_NOBITS"]
        wanted_sections = ["SHT_PROGBITS"]
        for section in ELFFile(elffile).iter_sections():
            found = False
            segment_name = ""
            segment_count = 0
            for segment in segments_of_interrest:
                if segment.section_in_segment(section):
                    found = True
                    segment_name = f"{segment.header['p_type']}-{segment_count}"
                    break
                segment_count += 1
            if found and section.header['sh_type'] in wanted_sections:
                print(f"Segment: {segment_name}, section: {section.name}, type: {section.header['sh_type']}, data size: {section.data_size}, offset: ???")
                print(len(section.data()))
                if len(section.data()) == 32:
                    print(section.data())
                data_found = (mm.find(section.data()) != -1)
                print(f"Data found: {data_found}")
                #sys.exit(0)

                #n = section.num_symbols()
                #for i in range(0, n):
                #    print(f"Symbol: {i}")
            #if segment.header.p_filesz != segment.header.p_memsz:
            #    seg_head = segment.header
            #    print(f"Type: {seg_head.p_type}\nOffset: {hex(seg_head.p_offset)}\nSize in file:{hex(seg_head.p_filesz)}\nSize in memory:{hex(seg_head.p_memsz)}")

