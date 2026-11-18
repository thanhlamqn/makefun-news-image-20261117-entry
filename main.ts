// news-image-20261117 entry (Node 22, standard library only).
//
// The entry is one image: entry.png beside this file sums up the world
// news of Tuesday 17 November 2026 — Iran's drone attack on the US radar
// base in Bahrain, the bridge war in Ukraine, Trump flying to APEC, the
// third US carrier in the Gulf, Japan scrambling jets, and the day's other
// stories. The image was drawn from real reports (see SOURCES.md); this
// program only copies it to the output directory, after checking it meets
// the competition's gate: a whole PNG of at most 1 MiB and at most
// 1024 by 1024 pixels. The grader runs with no network, so the image is
// baked into the repository and nothing is fetched at run time.
//
// Run it outside the grader's container with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1048576; // 1 MiB
const MAX_SIDE = 1024; // pixels

function pngSize(buf) {
  // A PNG's IHDR chunk holds width and height as big-endian uint32s at
  // offsets 16 and 20, and a whole PNG ends with its IEND chunk. Fail
  // loudly on anything that is not a complete PNG.
  if (buf.length < 24 || buf.toString('latin1', 1, 4) !== 'PNG') {
    throw new Error('entry.png is not a PNG file');
  }
  // A PNG's last 12 bytes are its IEND chunk: 4 length bytes, "IEND",
  // then the CRC. "IEND" itself sits at length-8.
  if (buf.toString('latin1', buf.length - 8, buf.length - 4) !== 'IEND') {
    throw new Error('entry.png is truncated: no IEND chunk');
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

const here = new URL('.', import.meta.url);
const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const bytes = statSync(source).size;
if (bytes > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB gate`);
}
const { width, height } = pngSize(readFileSync(source));
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 gate`);
}

copyFileSync(source, target);
console.log(`wrote ${target} (${width}x${height}, ${bytes} bytes)`);
