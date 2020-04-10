# fire-app

Bushfire Volunteer Management Application (TL 20-S1-2-C Fire App)

A web app to assist with firefighting scheduling activities

https://redmine.cecs.anu.edu.au/redmine/projects/bushfire-volunteer-management-application


# Development Environment Setup

The recommended development environment we will be using is a combination of Docker and VScode.
This guide is for setting these up on Windows, aimed at people who have not used Docker before.

This may take an hour or two.

## Setup Hyper-V

Hyper-V is a pre-requisite for docker and may need to be enabled.

First, open the command prompt and run the command 'system info'.
At the bottom there should be a checklist of Hyper-V requirements.
You may need to enable Hyper-V at the BIOS level before the Windows level.

### If your windows version is Windows Education or Professional
You should be able to enable Hyper-V now.

If you are using Windows Home, do the next step first.

In the windows start menu type 'windows features' and open 'Turn Windows features on or off'.

A list will be presented. Search for 'Hyper-V' and make sure it is checked.

After enabling it, windows may ask you to restart.

### If your windows version is Windows Home
There are some extra steps required to enable hyper-v and install docker.

First we need to download the Hyper-V packages for windows. We will use some .bat files to make this simple.

Here is the link for the [Hyper-V package downloader](https://drive.google.com/open?id=1ndzL35iJgxk7pEKbi_sDvgbSFNklEQq8).

Here is the link for the [containers package downloader](https://drive.google.com/open?id=1YfmvwxJ9OuXq676V8_6MldwAFG_xCL1T). (Not sure if this is required)

Run these scripts as administrator. They will both ask you to restart after finishing. Restart after finishing both.

Now Hyper-V will be available for you to enable in the above step

## Setup Docker

Start downloading docker desktop for windows from this [link](https://hub.docker.com/editions/community/docker-ce-desktop-windows).
On the right there is a 'Get Docker' button.

### If you are using Windows 10 Home
While this downloads, there is an extra step required to trick the docker installer that you are using Windows Professional.
We need to temporarily edit two registry Keys.

In the windows start menu type 'regedit' and open the Registry Editor.

```
Change in \HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion :

EditionID: Core --> Professional

ProductName: Windows 10 Home --> Windows 10 Pro
```

After reseting my PC these keys changed back automatically,
you'd want to make sure they are reset after installing docker.

### Once docker has finished downloading
Step though the installer to install it.

After it installs run docker, this will create an icon in the system tray.
Docker may take a while to start, once it has the icon will stop animating.

Click on the icon, ensure that one of the options is 'Change to Windows containers...',
If one of the options is 'Change to Linux containers...' click it.

### Changing Docker settings
Click on the icon, and open settings.

You may want to disable docker from starting when you logon.
Docker takes a lot of system resources, you really only want it on when you are developing.

In the shared drives tab, you will need to tick a drive.
If you have multiple drives it should be the one that you will clone this gitlab repository to.
Click Apply.

In the advanced tab you can change how many system resources Docker takes when it is running.
I have found that if you have too many programs running before you start docker,
sometimes docker fails to start because it requires too many resources.

Docker is now configured

## Setup VSCode
Install VS code from this [link](https://code.visualstudio.com/).
Select 'Download for Windows, stable build'.

You may already have it installed from COMP2300.

Install the extension 'Remote Development' by Microsoft.
This enables VS to manage the docker containers for you.
Connecting the open project to a docker container without you having to learn all the docker commands.

## Demonstration
Clone this repository to you local pc and open the project/folder with VScode.

In the '.devcontainers' folder of the repository is the docker configuration used by VScode.
This configuration may change over time.

In the bottom left there is a green button. Click this, it will show you a few commands.
Run 'Remote-Containers: Reopen in Container'.

This will start opening the project in a linux container.
If this is the first time running on the pc, or the '.devcontainers' configuration has changed,
This might take a little while because the container needs to be built. Otherwise it is quite fast.

You can click on the 'Installing Dev container (details)' to see the steps being taken to run docker.
If you're worried that the process has hanged for some reason,
it is safe to click the green button in the bottom left, select 'Close Remote Connection' and try to start the container again.


# Running the App



