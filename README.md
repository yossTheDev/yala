<h1 align="center">yala</h1>

![screenshot](/img/banner.png)
<p align="center"> The Most Prettier, TUI based 📦 Package Manager for <b>Arch Linux</b> and <b>Derivates</b>. Inpired by <a href="https://github.com/volitank/nala">Nala</a></p>

<div align="center">
<img alt="GitHub" src="https://img.shields.io/github/license/yossthedev/yala?style=for-the-badge">
<img alt="GitHub" src="https://img.shields.io/github/license/yossthedev/yala?style=for-the-badge">
<img alt="GitHub" src="https://img.shields.io/github/license/yossthedev/yala?style=for-the-badge">
</div>

```monospace
⚠️ yala is currently under development so expect drastic changes and some bugs
```

## 🚀 Features

* 🎨 Pretty outputs
* 🙂 Ease to use and intuitive commands
* 📦 Basic Commands -> Install, Search, Update, Upgrade
* 🏗️ Advanced Commands -> Inspect, more comming soon...

---

## 💡 The IDEA

The idea behind **Yala** is to create a package manager more intuitive, beautiful, and with additional features to make our life easier. Like Inspecting Packages, Advanced Logs, Unlocking Databases, Clearing Package Cache and more, some are already implemented and others are still to come.

----

## 👷‍♂️ Building From Source

First, make sure all dependencies are sucefully installed, I recommend [Poetry](https://python-poetry.org/) for enviroment configuration.

### Prepare Enviroment and Installing Dependencies

``` sh
poetry install
```

### Building with **PyInstaller**

Tested with **Python 3.11** and [PyInstaller](https://pyinstaller.org) **5.13.0**

``` sh
bash build.sh
```

### Building with **Nuitka**

Longer compile time but best performance and smaller compiled size. See [Nuitka Requirements](https://www.nuitka.net/doc/user-manual.html#requirements)

Installing Nuitka:

``` sh
python -m pip install nuitka  
```

Tested with **Python 3.11** and **Nuitka 1.7**

``` sh
bash build_nuitka.sh
```

## 👥 Contribution

All contributions are welcome, do not hesitate to give your comments about the developments of **Yala** or collaborate by reporting bugs or writing code. Thank you very much 😄

## ⚖️ License

---
![GPLv3](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)

```monospace
Yala is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License

Yala is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Yala. If not, see <https://www.gnu.org/licenses/>.
```
