# The World in One Page — Saturday 21 November 2026

A broadsheet summing up the world news of Saturday 21 November 2026,
drawn as one 1024x1024 image.

Stories: Russia's mass missile and drone strike on Ukraine, with missiles
landing in Poland; the AI stock selloff that pushed the S&P 500 into
correction; the International Court of Justice finding Myanmar responsible
for genocide against the Rohingya; the COP31 climate talks deadlocked over
fossil fuels in Antalya; the UK and EU signing their biggest post-Brexit
agreements; and a pancreatic cancer pill trial in which tumours became
undetectable in one in twelve patients.

Run it with:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

`gen.py` draws `entry.png` with PIL and the DejaVu fonts; `main.ts` runs
it and copies the PNG to the output directory. The output is
deterministic: two runs produce byte-identical files.
