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
python verta.py --elf ../test/zephyr/b_u585i_iot02a/tfm_ipc/build/tfm/bin/bl2.elf ../test/zephyr/b_u585i_iot02a/tfm_ipc/build/tfm/bin/tfm_s.elf ../test/zephyr/b_u585i_iot02a/tfm_ipc/build/zephyr/zephyr.elf \
--hex ../test/zephyr/b_u585i_iot02a/tfm_ipc/build/tfm_merged.hex --output test.hd -s
```

The above commands gets the sections from the provided elf files,
converts the provided hex file into a bin file, dumps it and decorates it with the found sections.

The -s options only prints the lines which contain the beginning of sections.

Example output:
```
c012000 4200 dec0 4200 dec0 0000 0000 0000 0000 Section: .BL2_NVMCNT (0xc012000)
c014000 3052 0330 354b 010c 057e 010c e762 020c Section: .text (0xc014000)
c0143d0 16db 2b19 a3eb 0803 4b45 38bf 2246 4ff0 Section: device_handles (0xc0143dc)
c014400 02b0 bde8 f087 08f1 0800 6844 1844 10f8 Section: .TFM_VECTORS (0xc014400)
c014450 0122 5b69 01a9 05eb 0900 9847 0028 cfdb Section: rodata (0xc014458)
c014800 45fd 00f0 33fd 0546 fff7 42ff 0446 2846 Section: .copy.table (0xc014804)
c014820 05f0 1cff 08b1 00f0 31fd 00f0 1ffd 0546 Section: .zero.table (0xc014828)
c014840 a342 01d0 00f0 22fd 6946 9df8 0800 00f0 Section: .TFM_SP_LOAD_LIST (0xc014848)
c0148f0 fff7 4afd 3046 03b0 f0bd 4ff4 0052 c168 Section: datas (0xc0148f8)
c014930 e6e7 4ff0 ff36 dde7 054b 0020 1a68 4ff0 Section: device_states (0xc01493c)
c014970 5b18 0a49 9b1a 0968 0360 b1fb f5f1 9942 Section: k_heap_area (0xc014970)
c014980 074b 04d2 0025 1968 0560 0131 1960 1868 Section: k_mutex_area (0xc014984)
c014990 2260 30bd 4021 0330 4421 0330 2000 0330 Section: .comment (0xc014998)
c0149b0 c4f8 9430 d4f8 9430 03f0 0403 0093 009b Section: .debug_aranges (0xc0149b8)
c014a60 fee7 fee7 fee7 fee7 fee7 fee7 fee7 fee7 Section: .TFM_PSA_ROT_LINKER (0xc014a60)
c015950 c420 2244 82f8 bca0 94f8 c430 73b1 e218 Section: .debug_info (0xc015958)
c018860 1502 56bf d3f8 f420 9a68 1204 02f0 7042 Section: .ER_TFM_CODE (0xc018860)
c01b6d0 0100 0000 fcb6 010c 0000 0330 1c01 0000 Section: .copy.table (0xc01b6d4)
c01b6e0 0000 0000 0000 0000 0000 0000 1c01 0330 Section: .zero.table (0xc01b6ec)
c026000 0000 0000 0040 0708 e03f 0f08 0200 0000 Section: .BL2_NoHdp_Code (0xc026000)
c027000 1281 dec0 0001 0203 0405 0607 0809 0a0b Section: .BL2_OTP (0xc027000)
c02a000 4200 dec0 4200 dec0 0000 0000 0000 0000 Section: .BL2_NVM (0xc02a000)
c0300b0 ffff ffff ffff ffff ffff ffff ffff ffff Section: rom_start (0xc0300b4)
c0306e0 ffff ffff ffff ffff ffff ffff ffff ffff Section: text (0xc0306e8)
c033e20 ffff ffff ffff ffff ffff ffff ffff ffff Section: initlevel (0xc033e24)
c033eb0 ffff ffff ffff ffff ffff ffff ffff ffff Section: devices (0xc033ebc)
c033ff0 ffff ffff ffff ffff ffff ffff ffff ffff Section: sw_isr_table (0xc033ff4)
c0343d0 ffff ffff ffff ffff ffff ffff ffff ffff Section: device_handles (0xc0343dc)
c034400 0024 0230 3547 030c 1d92 030c e989 030c Section: .TFM_VECTORS (0xc034400)
c034450 e989 030c 4546 030c 4746 030c 4946 030c Section: rodata (0xc034458)
c034800 4848 030c 20dd 030c 40ba 0230 5001 0000 Section: .copy.table (0xc034804)
c034820 2000 0230 2000 0000 a0bb 0230 f417 0000 Section: .zero.table (0xc034828)
c034840 0000 0230 0400 0000 0101 5f5f 0301 0000 Section: .TFM_SP_LOAD_LIST (0xc034848)
c0348f0 0008 0000 0000 0000 0300 0000 0100 0000 Section: datas (0xc0348f8)
c034930 0100 0000 0101 5f5f 0101 0000 1f01 0000 Section: device_states (0xc03493c)
c034970 0100 0000 8570 030c 0100 0000 0001 5f5f Section: k_heap_area (0xc034970)
c034980 0401 0000 1f03 0000 6586 030c 0005 0000 Section: k_mutex_area (0xc034984)
c034990 0000 0000 0000 0000 0300 0000 0000 0000 Section: .comment (0xc034998)
c0349b0 4000 0000 0005 0000 0100 0000 0000 0000 Section: .debug_aranges (0xc0349b8)
c034a60 38b5 0025 0648 2946 00f5 8054 d4f8 0024 Section: .TFM_PSA_ROT_LINKER (0xc034a60)
c035950 70bd 6ff0 8000 fae7 37b5 0024 0139 0129 Section: .debug_info (0xc035958)
c038860 7047 0000 bff3 4f8f 0549 064b ca68 02f4 Section: .ER_TFM_CODE (0xc038860)
c03e000 009a 394b 9a42 0fd1 eff3 1483 0cb4 1fb5 Section: .TFM_UNPRIV_CODE (0xc03e000)
c056a00 0122 e5f7 dbfc 1fbd 1fb5 1f48 6946 f7e7 Section: .psa_interface_cross_call (0xc056a00)
c071c80 7fe9 7fe9 ccf7 bcb9 7fe9 7fe9 ccf7 ceb9 Section: .gnu.sgstubs (0xc071c80)
```

