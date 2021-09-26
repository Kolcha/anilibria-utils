simple Python package to download torrent files from https://www.anilibria.tv/

```python
import anilibria

ts = anilibria.download_torrents('https://www.anilibria.tv/release/steins-gate-zero.html')
for name, data in ts:
    with open(name, "wb") as f:
        f.write(data)
```
