simple Python package to download torrent files from https://www.anilibria.tv/

```bash
python -m anilibria 'https://www.anilibria.tv/release/steins-gate-zero.html'
```

pass `--help` for possible options:

```bash
python -m anilibria --help
```

or use it in your own script:

```python
import anilibria

ts = anilibria.download_torrents('https://www.anilibria.tv/release/steins-gate-zero.html')
for name, data in ts:
    with open(name, "wb") as f:
        f.write(data)
```
