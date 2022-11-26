# Wallpaper Chan

A python app for auto downloading and changing anime wallpapers. This app only works on windows.

## Build

Clone the repository to your device and run the using:

```shell
git clone "https://github.com/Nadim147c/Wallpaper-Chan"
pip install -r requirements.txt
python main.py
```

Use `pyinstaller` to convert it to exe.

```
pip install pyinstaller
```

Follow [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging) packaging rules. Also include the assets folder using `--add-data`. Building command will look like this.

```shell
pyinstaller --noconfirm --onedir --windowed --icon "assets/colored_main.ico" --name "Wallpaper Chan" --add-data "assets;assets/" --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  main.py
```

## License

Licensed under [MIT](LICENSE) license.
