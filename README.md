<div align="center">
<picture>
  <img src="https://github.com/Haru3S/Source-Footsteps/blob/main/.github/src/icons/H3S%20Logo%20DUALTONE.svg?raw=true" height="100" />
</picture>
</div>

<h3 align="center">Source-Footsteps</h3>

<h6 align="center">/sɔɹs ˈfʊtˌstɛps/</h6>

<p align="center">
    <img src="https://github.com/Haru3S/Source-Footsteps/blob/main/.github/src/macchiato.png?raw=true" width="400" />
</p>

<p align="center">
  <a href="https://github.com/Haru3S/Source-Footsteps/stargazers">
    <img src="https://img.shields.io/github/stars/Haru3S/Source-Footsteps?colorA=363a4f&colorB=b7bdf8&style=for-the-badge&logo=data:image/svg+xml;base64,[SVG_BASE64]">
  </a>
  <a href="https://github.com/Haru3S/Source-Footsteps/releases/latest">
    <img src="https://img.shields.io/github/v/tag/Haru3S/Source-Footsteps?colorA=363a4f&colorB=a6da95&style=for-the-badge&logo=github&logoColor=cad3f5&label=Release">
  </a>
  <a href="https://github.com/Haru3S/Source-Footsteps/blob/main/LICENSE.md">
    <img alt="GitHub License" src="https://img.shields.io/github/license/Haru3S/Source-Footsteps?style=for-the-badge&labelColor=363a4f&color=f5a97f">
  </a>
</p>

**Source-Footsteps** is a small CLI program meant to take footstep samples and bake them into a single audio clip for use with audio effects in third-party programs. Source-Footsteps is inspired by the [Source Engine](https://developer.valvesoftware.com/wiki/Team_Fortress_2_engine_branch).

This program was also made out of sheer frustration, as I could not find an existing free program that did what I wanted. So, I'm making this project free and open source for anybody who needs this really specific niche.

## 📦 Installing

### Standalone

You can download the prebuilt Windows executable under [Releases](https://github.com/Haru3S/Source-Footsteps/releases).

Extract the `.zip`, place your samples in the `footsteps` folder, and then run `SourceFootGen.exe`.

### Building from Source

Download the repository as a `.zip` file and extract it, or clone the repository:

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

The compiled executable will be located at `dist/SourceFootGen.exe`.

Create a `footsteps` folder next to the executable and place your `.wav` samples inside it.

## 📖 How to Use

> [!TIP]
> The program is unaware of material types, so only provide samples of the material you want to generate.

> [!TIP]
> `.wav` files are recommended.

**Duration:** How long you want the baked track to be.

**Tail Length:** How much extra track length you want for reverb/delay effects.

<img src="https://github.com/Haru3S/Source-Footsteps/blob/main/.github/assets/tail.png?raw=true">

**Step Interval:** How much time there is between each sample.

### Third-Party Samples

- [Half-Life 2 Footsteps](https://github.com/sourcesounds/hl2/tree/master/sound/player/footsteps)
- [Team Fortress 2 Footsteps](https://github.com/sourcesounds/tf/tree/master/sound/player/footsteps)

## 🖼️ Screenshots

<img src="https://github.com/Haru3S/Source-Footsteps/blob/main/.github/assets/screenshot1.png?raw=true">

<img src="https://github.com/Haru3S/Source-Footsteps/blob/main/.github/assets/screenshot2.png?raw=true">

## 🌟 Credits

Inspiration: [**Source SDK 2013**](https://github.com/ValveSoftware/source-sdk-2013) by Valve Software

My cat: **Kiki**

