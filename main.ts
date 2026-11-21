// News-image entry for Saturday 21 November 2026 (Node 22, standard
// library only). The broadsheet is drawn by gen.py in this same directory:
// this entrypoint runs it, then copies the PNG it writes to the output
// directory the grader gives us. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// gen.py is deterministic (fixed fonts, no network, no randomness), so the
// two grading runs write identical bytes.

import { copyFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Draw the broadsheet first; gen.py writes entry.png beside this file.
execFileSync('python3', [join(here, 'gen.py')], { stdio: 'inherit' });

copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
