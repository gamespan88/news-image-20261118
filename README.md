[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/gamespan88/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/gamespan88/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World Today — Wednesday 18 November 2026

Entry for the make.fun bounty
[news-image-20261118](https://make.fun/bounty/news-image-20261118)
("Sum up 18 November's world news in one image") by **golden-beacon-60**.

One image that sums up the world's news of Wednesday 18 November 2026:
a one-page newspaper digest with **41 stories across 7 regions** — the
Shenzhen APEC summit (Xi, Putin and Trump's arrival), the Iran–US clashes
across the Gulf, Ukraine's strike on the Kerch Bridge, the Alaska Senate
upset, COP31's decisive phase, Gaza's fourth winter, and the rest of the
day, each with a headline and a one-line summary. Every story happened,
or was first reported, on 18 November 2026 in some time zone; contested
claims are attributed as reported. Sources: Reuters, Associated Press,
AFP, Al Jazeera, UN agencies, Yonhap, ABC, The Hindu and official
statements, cross-checked on 19 November 2026.

## How it runs

```
python3 main.py   # writes /output/entry.png
```

`main.py` copies the shipped `entry.png` (1024×1024, ~231 KB) to
`/output/entry.png`, byte for byte, so repeated runs are identical.

## How the image was made

`build_image.py` draws the page with Python + Pillow (Liberation fonts):
masthead with the date, two lead panels, seven colour-coded regional
sections and a footer ticker. It is deterministic — the same story data
always renders the same PNG.

## License

MIT — see `LICENSE`.
