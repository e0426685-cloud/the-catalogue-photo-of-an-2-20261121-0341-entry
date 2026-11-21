# The Perpetual Power Strip

[![make.fun · the-catalogue-photo-of-an-2-20261121-0341](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341?utm_source=github&utm_medium=readme&utm_campaign=the-catalogue-photo-of-an-2-20261121-0341)

A catalogue photograph of an impossible gadget: **The Perpetual Power Strip** —
a white power strip that plugs into itself and powers a phone from nothing.
Rendered as a studio product shot with PIL: soft warm-grey seamless sweep,
top-left key light, contact shadows, and exactly one accessory — a smartphone
standing upright, screen lit at 100%.

## How to run

```sh
python3 main.py
```

Writes `/output/entry.png` (1024x1024 PNG, under 1 MiB). Python 3.13,
standard library + Pillow only, no network, fully deterministic.
