# Prerequisites

## Attack Tools 

### Python3
- **Linux:** `sudo apt install python3`
- **macOS:** [Installation Guide](https://docs.brew.sh/Homebrew-and-Python)

### Burp (Community edition)
- **All OS:** [Download page](https://portswigger.net/burp/releases/professional-community-2025-1-1?requestededition=community&requestedplatform=)

### Dirbuster
- **Linux:** `sudo apt install dirb`
- **MacOS:** `brew install gobuster` (Unfortunately, dirbuster doesn't exists on MacOS...)

### FFUF (Fuzz Faster U Fool)
- **Linux:** `sudo apt install ffuf`
- **MacOS:** `brew install ffuf` 
- [Documentation](https://github.com/ffuf/ffuf)


---

## Apache Configuration Prerequisites

### Update `/etc/hosts`
Open your `/etc/hosts` file with admin privileges before adding these lines:
```/etc/hosts
::1 attack.local www.attack.local
```

### Create a dedicated vhost `/etc/apache2/sites-available/attack-vhost.conf`
Ensure to replace `path_to_local_projet` by your own path:
```/etc/apache2/sites-available/attack-vhost.conf
<VirtualHost *:9997>
    ServerName attack.local
    DocumentRoot "/path_to_local_projet"

    <Directory "/path_to_local_projet">
        AllowOverride All
        Require all granted
    </Directory>

</VirtualHost>
```
<em>Don't forget to restart Apache afterwards.</em>

### Add an AV exclusion
For the attacks to proceed correctly, it is necessary to set up exceptions 
to the project root folder:
- <em>**/path_to_local_projet/**</em>
