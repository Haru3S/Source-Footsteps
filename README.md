<div align="center">
<picture>
  <img src="https://github.com/Haru3S/Source-Footsteps/blob/main/.github/src/icons/H3S%20Logo%20DUALTONE.svg?raw=true" height="100" />
</picture>
</div>

<h3 align="center">Source-Footsteps</h3>

<h6 align="center">/sɔɹs ˈfʊtˌstɛps/</h6>

<p align=center>
    <img src="https://github.com/Haru3S/Source-Footsteps/blob/main/.github/src/macchiato.png?raw=true" width="400" />
</p>

<p align="center">
  <a href="https://github.com/Haru3S/Source-Footsteps/stargazers">
    <img src="https://img.shields.io/github/stars/Haru3S/Source-Footsteps?colorA=363a4f&colorB=b7bdf8&style=for-the-badge&logo=data:image/svg+xml;base64,[SVG_BASE64]">
  </a>
  <a href="https://github.com/Haru3S/Source-Footsteps/releases/latest">
    <img src="https://img.shields.io/github/v/tag/Haru3S/AstraHUD?colorA=363a4f&colorB=a6da95&style=for-the-badge&logo=github&logoColor=cad3f5&label=Release">
  </a>
  <a href="https://github.com/Haru3S/Source-Footsteps/blob/main/LICENSE.md">
    <img alt="GitHub License" src="https://img.shields.io/github/license/Haru3S/Source-Footsteps?style=for-the-badge&labelColor=363a4f&color=f5a97f">
  </a>
</p>  

<p align="center">

**Source-Footsteps** is a small CLI script meant to take inputted footstep samples and bake them into one clip for audio effects on third party programs. Source-Footsteps is inspired by the [Source Engine](https://developer.valvesoftware.com/wiki/Team_Fortress_2_engine_branch).

Also this program was made from shear frustration as I could not find a existing or free program that did what I wanted to do, so I'm making this project free and open source for anybody that needs this really specific niche.

## Installing

### Standalone

You can download the prebuilt Windows executable under [Releases](https://github.com/Haru3S/Source-Footsteps/releases).

### Building from Source

Download the repository as a ZIP file and extract it, or clone the repository:

```bash
git clone https://github.com/Haru3S/Source-Footsteps.git
```

Install the required dependencies:
```bash
python -m pip install -r requirements.txt
```
Build the executable using PyInstaller:
```bash
python -m PyInstaller --onefile --name SourceFootGen main.py
```
The compiled executable will be located at `dist/
SourceFootGen.exe`.

Create a `footsteps` folder next to the executable and place your `.wav` samples inside it.

</p>