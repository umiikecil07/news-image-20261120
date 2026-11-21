// News-image entry (Node 22, standard library only).
// Entry: The World Today — Friday 20 November 2026.
// The image is drawn by generate_image.py and stored here as entry.png;
// this program copies it byte-for-byte to /output/entry.png, so the
// judge sees exactly the file in this repository. The copy is
// deterministic: the same input bytes always produce the same output.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) {
  throw new Error('entry.png is missing from this repository');
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
