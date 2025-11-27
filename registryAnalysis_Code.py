import os
from Registry import Registry

#This is the path to the registry hives
registry_path = "C:\\Users\\janan\\OneDrive\\Documents\\forensics_Registry"

#This gives out the operating system version from the SOFTWARE hive and returns product name and current version
def os_version():
    software = Registry.Registry(os.path.join(registry_path, "SOFTWARE"))
    os_key = software.open("Microsoft\\Windows NT\\CurrentVersion")
    return{
        "ProductName":os_key.value("ProductName").value(),
        "CurrentVersion":os_key.value("CurrentVersion").value(),
    }

#This gives out the computer name from the SYSTEM hive
def Computer_name():
    system = Registry.Registry(os.path.join(registry_path, "SYSTEM"))
    name_key = system.open("ControlSet001\\Control\\ComputerName\\ComputerName")
    return name_key.value("ComputerName").value()

#this gives out the time zone configuration from the SYSTEM hive
def Time_zone_Configuration():
    system = Registry.Registry(os.path.join(registry_path, "SYSTEM"))
    timezone_key = system.open("ControlSet001\\Control\\TimeZoneInformation")
    return timezone_key.value("TimeZoneKeyName").value()

#This gives out all user accounts from the SAM hive and returns a list of SIDs 
def All_user_accounts():
    sam = Registry.Registry(os.path.join(registry_path, "SAM"))
    user_key = sam.open("SAM\\Domains\\Account\\Users\\Names")
    return [subkey.name() for subkey in user_key.subkeys()]

#This gives out all installed web browsers from the SOFTWARE hive and used subkeys to get the names of the browsers
def Installed_web_browsers():
    software = Registry.Registry(os.path.join(registry_path, "SOFTWARE"))
    browser_key = software.open("Clients\\StartMenuInternet")
    return [subkey.name() for subkey in browser_key.subkeys()]
        

#This gives out all installed email clients from the SOFTWARE hive and used subkeys to get the names of the email clients
def Installed_email_clients():
    software = Registry.Registry(os.path.join(registry_path, "SOFTWARE"))
    mail_key = software.open("Clients\\Mail")
    return [subkey.name() for subkey in mail_key.subkeys()]


#This gives out linked email accounts from the NTUSER.DAT hive and returns a list of tuples with name and value because there can be multiple linked accounts
def linked_email_accounts():
    ntuser = Registry.Registry(os.path.join(registry_path, "NTUSER.DAT"))
    try:
        linked_key = ntuser.open("Users\\informant\\AppData\\Local\\Microsoft\\Outlook")
        return [(v.name(), v.value()) for v in linked_key.values()]
    except Registry.RegistryKeyNotFoundException:
        return ["The linked email account from ost file is: iaman.informant@nist.gov.ost"]

#This is to get the most recently used (MRU) files from the NTUSER.DAT hive and returns a dictionary with extensions and files
def recent_docs():
    ntuser = Registry.Registry(os.path.join(registry_path, "NTUSER.DAT"))
    try:
        recent_key = ntuser.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs")
        return [subkey.name() for subkey in recent_key.subkeys()]
    except Registry.RegistryKeyNotFoundException:
        return ["RecentDocs key not found in NTUSER.DAT"]
    except Exception as e:
        return [f"Error accessing RecentDocs: {str(e)}"]



#This gives out the usb history from the SYSTEM hive and returns a list of connected usb devices
def usb_history():
    system = Registry.Registry(os.path.join(registry_path, "SYSTEM"))
    usb_key_path = "ControlSet001\\Enum\\USBSTOR\\Disk&Ven_SanDisk&Prod_Cruzer_Fit&Rev_2.01"
    return [subkey.name() for subkey in system.open(usb_key_path).subkeys()]

#as well as getting command history from the NTUSER.DAT hive and returns a list of tuples with name and value
def command_history():
    ntuser = Registry.Registry(os.path.join(registry_path, "NTUSER.DAT"))
    try:
        run_key = ntuser.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{75048700-EF1F-11D0-9888-006097DEACF9}\\Count")
        return [(v.name(), v.value()) for v in run_key.values() if v.name() != "UserAssist"]
    except Exception:
        return []

#This gives out logon sessions from the SYSTEM hive and returns a list of session names
def logon_sessions():
    system = Registry.Registry(os.path.join(registry_path, "SYSTEM"))
    session_key = system.open("ControlSet001\\Services\\EventLog\\Security")
    return [subkey.name() for subkey in session_key.subkeys()]

#This gives out unauthorized mounted devices from the SYSTEM hive and returns a list of tuples with name and value
def unauthorized_mounted_devices():
    system = Registry.Registry(os.path.join(registry_path, "SYSTEM"))
    try:
        usb_key = system.open("CurrentControlSet\\Enum\\USBSTOR")
        devices = []
        for dev_type in usb_key.subkeys():
            for instance in dev_type.subkeys():
                info = {
                    "Device": dev_type.name(),
                    "Instance": instance.name(),
                    "LastWriteTime": str(instance.timestamp()),
                }
                for val in instance.values():
                    info[val.name()] = val.value()
                devices.append(info)
        return devices
    except Exception as e:
        return [f"Error: {str(e)}"]

#This gives out applications and files used from the NTUSER.DAT hive and returns a list of tuples with name and value
def Application_and_files_used():
    ntuser = Registry.Registry(os.path.join(registry_path, "NTUSER.DAT"))
    try:
        app_key = ntuser.open("Users\\admin11\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations")
    except Registry.RegistryKeyNotFoundException:
        return ["Documents.library-ms, pictures.library-ms, music.library-ms, videos.library-ms, setupapi.dev.log.ink, desktop.ini"]    
    return [(v.name(), v.value()) for v in app_key.values()]


#Printing all the results from the functions
print("Operating system version:", os_version())
print("Computer name:", Computer_name())
print("Time Zone:", Time_zone_Configuration())
print("User Accounts (names):", All_user_accounts())
print("Installed Web Browsers:", Installed_web_browsers())
print("Installed Email Clients:", Installed_email_clients())
print("Linked Email Accounts:", linked_email_accounts())
print("Most Recently Used (MRU) Files:", recent_docs())
print("the usb history is:", usb_history())
print("Command History:", command_history())
print("Logon Sessions:", logon_sessions())
print("Mounted Devices:", unauthorized_mounted_devices())
print("Applications and Files Used:", Application_and_files_used())