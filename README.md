[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/umiikecil07/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/umiikecil07/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World Today — 20 November 2026

A single-image summary of 20 November 2026's world news, laid out as a
one-page newspaper front page: **"THE WORLD TODAY — Friday 20 November
2026"**. Six stories and a news ticker cover the day's biggest headlines,
set in a clean broadsheet design that reads at a glance.

The image is a fixed 1024×1024 PNG (`entry.png`), shipped with the entry;
`main.ts` publishes it to the output directory make.fun expects.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies `entry.png` to `out/entry.png`. Without
`MAKEFUN_OUTPUT_DIR` set, the image is written to `/output/entry.png`.

## Stories

Six stories from Friday 20 November 2026, each grounded in that day's
reporting: Russia's biggest overnight missile and drone attack on Kyiv;
the UN court's ruling that Myanmar committed genocide against the
Rohingya, the first such ruling against a state; the first three-way
Trump–Xi–Putin summit in Shenzhen and its joint peace declaration;
Anthropic's record Nasdaq debut followed by a slide as AI stocks sold
off; a Houthi missile damaging Riyadh's PIF Tower; and a tanker ablaze
in the Strait of Hormuz as the Iran war enters its ninth month. The
ticker notes Trump's pardon of baseball legend Pete Rose, the EU
summoning Russia's envoy over embassy damage in Kyiv, and Kenya
discharging its last Ebola patient.

## Files

- `entry.png` — the newspaper front page (1024×1024)
- `main.ts` — publishes `entry.png` to `$MAKEFUN_OUTPUT_DIR`
- `generate_image.py` — draws `entry.png` with Python + Pillow (optional; already built)
- `LICENSE` — MIT

## License

MIT — see [LICENSE](LICENSE).
