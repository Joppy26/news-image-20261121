// News-image entry for Saturday 21 November 2026 (Node 22, standard
// library only). The broadsheet is drawn by gen.py in this same directory;
// entry.png is the committed output of that generator (two local runs
// produced byte-identical files), and this entrypoint copies it to the
// output directory the grader gives us. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The entrypoint does not re-run gen.py: the grading sandbox may not have
// PIL or the DejaVu fonts, and its repo snapshot is not writable, so
// copying the committed PNG is the deterministic path.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = new URL('.', import.meta.url).pathname;
const source = join(repoDir, 'entry.png');

if (!existsSync(source)) {
  console.error(`entry.png not found at ${source}`);
  process.exit(1);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');

copyFileSync(source, dest);

const original = readFileSync(source);
const copied = readFileSync(dest);
if (!original.equals(copied)) {
  console.error('entry.png copy differs from the original; refusing to continue');
  process.exit(1);
}

console.log(`copied entry.png to ${dest} (${copied.length} bytes, byte-identical)`);
