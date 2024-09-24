# arxd
Extract (and delete) archive files under present working directory.


### Usage
By default, the script will extract the archives into `prefix/archive filename`.

Prefix defaults to current directory.

That is, extraction of "flowers.zip" creates "flowers" directory with archive
contents under prefix directory.

- To specify custom prefix, use `-p` option.
```bash
arxd -p /path/to/prefix
```

- To delete the files after extraction, specify `-d` option.
```bash
arxd -d
```

- To ignore files, you can give regex pattern using `-i` option.
```bash
arxd -i PATTERN
```


### Installation
1. Clone the repository or download zip.
2. `cd` into project root.
3. Use your favourite python package manager to install. (See next step)
4. Run `pip install .` or `pipx install .` .
