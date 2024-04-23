# Energy Grabber by Ted - EGT
Hi my name is Ted.
This is a custom plugin i have created for fetching your provider's monthly energy cost per kwh from the internet. At the moment it is working just with a specific website.

# Version
The latest version is 1.1.0

# How to install via Download
- Press the Download at the top....
- Unzip and delete the "master" from the folder name
- Drop the folder inside the custom_components
- Restart Home Assistant
- Go to step 11.

# How to install - Manually
For now i am not interested into creating this as an AddOn and it is too soon for HACS.
Having that in mind, since i spent time to create this custom component, you will have to spend some time to install it. Let's go!

1. You need to have the add-on "Studio Code Server" installed.
2. Then open it and click on the "custom_components" folder under "Config".
3. Right click on the "custom_components" and choose "New Folder..." and you have to give the name "energy_grabber_by_ted"
4. Next you need to select that folder, right click on it and press "New File...". The file name should be "__ init __.py" TWO lower dashes before and after init without the spaces but with two lower dashes!
5. Next you need to select that folder again, right click on it and press "New File...". The file name should be "config_flow.py"
6. Next you need to select that folder again, right click on it and press "New File...". The file name should be "const.py"
7. Next you need to select that folder again, right click on it and press "New File...". The file name should be "manifest.json"
8. Next you need to select that folder again, right click on it and press "New File...". The file name should be "sensor.py"

9. When you are finished creating these files you need to copy - paste from this repository the code lines from each file to your local files.

10. You need to restart your home assistant....
11. Now go to "Settings" > "Devices & Services" > " + ADD INTEGRATION" and search for "Energy Grabber by Ted - ETG".
12. If everything went well, you will see it in the list and you have to click on it.
13. A pop-up form will show up with three fields...
    The first field is a URL for your provider's energy price. (Read below how to get the url you need)
    The second field is a friendly name for your sensor. My suggestion is to use something like "Protergia Οικιακό Value Simple Energy Cost" which is the name of the energy program you belong to.
    The third field is the provider's monthly fee for your program (πάγιο).
14. Press submit and if everything went well, you will see the integration added to your list and with the sensors inside.
15. You can add multiple instances of "Energy Grabber by Ted - EGT" so that you can track the monthly price changes from each provider.

A quick note, the prices get updated every 6 hours.


# How to get a url for my provider's pricelist
This integration is using the website https://www.tsig.gr/electricity
All you have to do is choose your provider (Εταιρεία), then choose your selected package (Τιμολόγιο, Ειδικό, Σταθερό..κτλ) and press "Εμφάνιση".
This will provide you a url like this.... "https://www.tsig.gr/electricity?company=Protergia&timologio=%CE%9A%CF%85%CE%BC%CE%B1%CE%B9%CE%BD%CF%8C%CE%BC%CE%B5%CE%BD%CE%BF"
Copy this url and paste it in the first field mentioned above in step 13.

# Important notes
I have absolutely no relationship with the website "tsig.gr".
I am not responsible for the validity of these prices.
This is a proof-of-concept project and provided as-is.

# Even more important notes
If you like this project, there are three ways you can thank me.

1. Buy me a Porsche
2. Buy me a cappuccino diplo metrio kastani, ligo kanela.
3. Say thank you!
4. All of the above.
