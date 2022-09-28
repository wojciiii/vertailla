#!/usr/bin/env python3
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You must provide this script with an elf binary file you want to examine")
        sys.exit(1)

    segments_of_interrest = []
    with open(sys.argv[1], 'rb') as elffile:
        for segment in ELFFile(elffile).iter_segments():
            if segment.header.p_type == "PT_LOAD":
                print(segment.header)
                segments_of_interrest.append(segment)

        wanted_sections = ["SHT_PROGBITS", "SHT_NOBITS"]
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
                print(f"Segment: {segment_name}, section: {section.name}, type: {section.header['sh_type']}, data size: {section.data_size}")
                for b in section.data():
                    print(hex(b))
                print(len(section.data()))
                #n = section.num_symbols()
                #for i in range(0, n):
                #    print(f"Symbol: {i}")
            #if segment.header.p_filesz != segment.header.p_memsz:
            #    seg_head = segment.header
            #    print(f"Type: {seg_head.p_type}\nOffset: {hex(seg_head.p_offset)}\nSize in file:{hex(seg_head.p_filesz)}\nSize in memory:{hex(seg_head.p_memsz)}")

