<h2 align="center">PyImg2epub</h2>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

This is a simple python script for creating epub files from chapters composed by images.

---

## 📝 Table of Contents

- [Setting up a local enviroment](#getting_started)
- [Usage](#usage)
- [Authors](#authors)



## 🏁 Getting Started <a name = "getting_started"></a>

To download the source code you just need to type this in a bash:

```console
matteopiffari@main:~$ git clone https://github.com/matteopiffari/PyImg2Epub
```

Install EbookLib:

```console
matteopiffari@main:~$ pip install EbookLib
```

Setup the input directory (`/chapters` in the default config)

To make the script work the directory must be structured in this way:

```md
chapters
├─── 001
│    ├─── 001.jpg
│    ├─── ...
│    └─── n.jpg
├─── 002
│    ├─── 001.jpg
│    ├─── ...
│    └─── n.jpg
├─── ...
└─── n
     ├─── 001.jpg
     ├─── ...
     └─── n.jpg
```

> You can also find this structure inside the file  `/chapters/STRUCT.md`


## 🎈 Usage <a name="usage"></a>

Before start you need to change some variables in the code:
- `TITLE`: the title of the book
- `AUTHOR`: the author of the book
- `DESCRIPTION`: the description or trama of the book
- `OUTPUT_DIR` (optional): the output directory where epub files will saved

After that you can run the script in this way:

```console
matteopiffari@main:~$ cd PyImg2Epub
matteopiffari@main:~/PyImg2Epub$ python main.py
```

> You will find the .epub files in the folder named `output` (or the one specified in the `OUTPUT_DIR` variable in the code)

## ✍️ Authors <a name = "authors"></a>

- [matteopiffari](https://github.com/matteopiffari) - Idea & Work
