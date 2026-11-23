# The World in One Day — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Indodegen/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Indodegen/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

Entry for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123) — a program that writes one image to `/output/entry.png`.

**The World in One Day — Monday 23 November 2026: 40 stories, 6 regions, every one dated that day.** A newspaper front page drawn entirely by code: COP31 ends with no deal and the blame game begins; Ukraine sinks the Russian corvette Merkury off Libya; Russian missiles fall inside Poland and NATO meets; Belgium's skies shut for 14 hours; the Serang candy-factory search goes on; Democrats win 258 House seats.

## How it works

- `generate.py` draws `entry.png` (1024×1024) with Pillow + Liberation fonts: masthead with the date, a stats strip, 3 lead stories, 10 more featured stories, a world dot-map, 27 more stories in a numbered list, and a DATE CHECK box naming what was left out because it belongs to an earlier day. No network, no randomness, no timestamps — running it twice writes byte-identical PNGs.
- `main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`.

## Run it

```sh
python3 generate.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters · AP · CNN · Le Monde · Al Jazeera · France24 · BusinessWorld · Just Security — all scenes drawn, not photographs. REPORTED = wires / on the record; CLAIM = one side's claim, named as such.

## License

MIT — see [LICENSE](LICENSE).
