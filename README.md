<h1 align="center">yala</h1>

![screenshot](/img/banner.png)
<p align="center"> The most prettier 📦 Package Manager for <b>Arch Linux</b> and <b>Derivates</b></p>

<img alt="GitHub" src="https://img.shields.io/github/license/yossthedev/yala?style=for-the-badge">

## 🚀 Features

* 🎨 Pretty outputs
* 🙂 Ease to use
* 📦 Basic Commands -> Install, Search, Update, Upgrade
* 🏗️ Advanced Commands -> Inspect, more comming soon...

## 👷‍♂️ Building From Source

First, make sure all dependencies are sucefully installed, I recommend Poetry for enviroment configuration.

### Prepare Enviroment and Installing Dependencies

``` sh
poetry install
```

### Building with **PyInstaller**

Tested with Python 3.11 and PyInstaller 5.13.0

``` sh
bash build.sh
```

### Building with **Nuitka**

Slow compile time but best performance and small compiled size

``` sh
python -m pip install nuitka  
```

Tested with Python 3.11 and Nuitka 1.7

``` sh
bash build_nuitka.sh
```

## License

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
