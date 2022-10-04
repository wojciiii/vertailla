# Vertailla

This is a (quick and dirty) tool used to compare generated hex file with elf files used to generate it.
Zephyr and TF-M uses a merged HEX file which is difficult to debug using just hexdump.

## Why?

Linking is sometimes like black magic. If it doesn't work it can be difficult to determine why.

I want to be able to determine if the linked ELF file and the resulting hex file contains the required parts of the ELF file and at which offsets.
Looking at hexdumps gets tedious fast and therefore this tool.

## Usage

```
python verta.py -h
usage: verta.py [-h] --elf ELF [ELF ...] --hex HEX [HEX ...] [--output OUTPUT] [--short] [--verbose]

verta: decorated hexdump.

options:
  -h, --help           show this help message and exit
  --elf ELF [ELF ...]  input, ELF files
  --hex HEX [HEX ...]  input, HEX file
  --output OUTPUT      output, file to write output to, default -
  --short, -s          short output
  --verbose, -v        verbose flag

```

```
python verta.py --elf ../test/zephyr/b_u585i_iot02a/tfm_ipc/build/tfm/bin/bl2.elf \
--hex ../test/zephyr/b_u585i_iot02a/tfm_ipc/build/tfm_merged.hex -s
```

The above commands gets the sections from the provided elf files,
converts the provided hex file into a bin file, dumps it and decorates it with the found sections.

The -s options only prints the lines which contain the beginning of sections.

Example output:
```
c012000 4200 dec0 4200 dec0 0000 0000 0000 0000 Section: .BL2_NVMCNT (0xc012000)
c014000 3052 0330 354b 010c 057e 010c e762 020c Section: .text (0xc014000)
c01b6d0 0100 0000 fcb6 010c 0000 0330 1c01 0000 Section: .copy.table (0xc01b6d4)
c01b6e0 0000 0000 0000 0000 0000 0000 1c01 0330 Section: .zero.table (0xc01b6ec)
c026000 0000 0000 0040 0708 e03f 0f08 0200 0000 Section: .BL2_NoHdp_Code (0xc026000)
c027000 1281 dec0 0001 0203 0405 0607 0809 0a0b Section: .BL2_OTP (0xc027000)
c02a000 4200 dec0 4200 dec0 0000 0000 0000 0000 Section: .BL2_NVM (0xc02a000)
```

