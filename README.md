# SilvaGunner Downloader
Simple python program to download SilvaGunner rips and automatically format them.

# How to download

Download the .exe from the [GitHub releases]("")

You can also run it after installing all the modules, or you can build it into an .exe with *pyinstaller*

```console
pyinstaller --onefile --windowed --icon=icon.ico --version-file=file_version_info.txt  silvagunner_downloader.py
```

(This is more for me, than for other ppl)
To create a new version file after updating *metadata.yml*
```console
create-version-file metadata.yml --outfile file_version_info.txt 
```

# How to use

After running/opening the SilvaGuner downloader a GUI pops up where you can put a YouTube URL of any normal SilvaGunner rip

The GUI:<br>
![image](https://user-images.githubusercontent.com/71491435/226747888-146fd923-524e-4efc-9540-65a1a56883a0.png)

Keep in mind the program will stop you from entering videos that are not from the [SilvaGunner]("https://www.youtube.com/@SiIvaGunner") channel.

Also videos that are not formatted in the ``{Track} - {Game}`` format, will probably not get formatted correctly or possibly throw an error. So stuff like "Credits - The SiIvaGunner All-Star Nuclear Winter Festival" or "My Last Message" will not work right now. However I'm planning to add a checkbox for the auto-formatting.

The auto-formatted song:<br>
![image](https://user-images.githubusercontent.com/71491435/226749753-24b6bd02-18ff-40ce-9899-37a16d1320c9.png)

# Planned
- Auto-generated Cover/Album covers (Probably from Thumbnail)
- Better looking GUI
- Checkbox to toggle the auto-formatting
- Maybe an override checkbox to enter the metadata yourself for specific videos

I am not affiliated with SilvaGunner in any shape of form, I just enjoy the rips they make and want to listen to them on Spotify through Local Files :)
