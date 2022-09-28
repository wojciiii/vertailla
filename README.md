# Vertailla
Tool used to compare generated bin or hex files with elf files used to generate them.

## Why?

Linking is sometimes like black magic. It works but I don't know why.

I want to be able to determine if the linked ELF file and the resulting .bin file contains the required parts of the ELF file and at which offsets.
Looking at hexdumps gets tedious fast and therefore this tool.

## Usage

vert <elf_file> <hex_file>
