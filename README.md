# arxd
Extract (and delete) archive files under present working directory.


### Usage
By default, the script will extract the archives into `prefix/archive filename`.

Prefix defaults to current directory.

That is, extraction of "flowers.zip" creates "flowers" directory with archive
contents under prefix directory.

- To start extraction, use `-e` option. Without this option, no extraction occurs.
```bash
arxd -e
```

- To specify custom prefix, use `-p` option.
```bash
arxd -e -p /path/to/prefix
```

- To delete the files after extraction, specify `-d` option.
```bash
arxd -e -d
```

More in help message with `-h` option.


### Installation
1. Clone the repository or download zip.
2. `cd` into project root.
3. Use your favourite python package manager to install. (See next step)
4. Run `pip install .` or `pipx install .` .
