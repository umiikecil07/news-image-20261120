// main.ts — entrypoint for the make.fun news-image-20261120 competition.
//
// The repository ships a pre-rendered newspaper image (entry.png,
// 1024x1024) drawn by generate_image.py. This program does not redraw
// anything: it simply copies that image to the output location the
// harness expects, so both runs produce byte-identical output.
//
// The destination directory comes from MAKEFUN_OUTPUT_DIR and falls back
// to /output. The program fails loudly if entry.png is missing, so a
// broken repository can never silently submit an empty image.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(import.meta.dirname, "entry.png");
const dest = join(outputDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (looked in ${source})`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, dest);
