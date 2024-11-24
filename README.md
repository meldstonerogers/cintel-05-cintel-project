# cintel-05-cintel
Cintel Project 5
Melissa Stone Rogers, [GitHub](https://github.com/meldstonerogers/cintel-05-cintel)

## Introduction
Professional project using python, shiny, and reactive.calc function to publish a reactive shiny app with continuous intelligence. 
Commands were used on a Mac machine running zsh. Project was guided by the following respository's by Dr. Denise Case: [basic app](https://github.com/denisecase/cintel-05-cintel-basic), [fancy app](https://github.com/denisecase/cintel-05-cintel-fancy), and [final CI app](https://github.com/denisecase/cintel-05-cintel).  


## Project Set Up and Dependency Management 
### Build project in GitHub
Create project repository in Github. Create a requirements.txt and .gitignore file for Python code. Add the following to your requirements.txt: 
- faicons 
- pandas
- pyarrow
- plotly
- scipy
- shiny
- shinylive 
- shinywidgets

Publish GitHub Pages for your project repository.
Create a docs folder within your repository to keep your GitHub Pages content separate from your main project files. Within your GitHub repository, select add file and create a docs folder with, **docs/.gitkeep**. This allows a folder to be created with no content. 

The following instructions borrowed from Dr. Cases's Continous Intelligence Course within NWSU's School of Computer Science and Information Systems: 

1. Go to the repository on GitHub and navigate to the **Settings** tab.
2. Scroll down and click the **Pages** section down the left.
3. Select branch main as the source for the site.
4. Change from the root folder to the docs folder to publish from.
5. Click Save and wait for the site to build.
6. Eventually, be patient, your app will be published and if you scroll to the top of the Pages tab, you'll see your github.io URL for the hosted web app. Copy this to your clipboard. 
7. Back on the main repo page, find the About section of the repo (kind of upper right).
8. Edit the "About" section of the repository to include a link to your hosted web app by using the Pages URL. 

### Clone repository to your machine
```zsh
git clone project.url
```
Verify Python version of Python 3
```zsh
python3 --version

```
```zsh
python3 -m venv venv
source venv/bin/activate
```
### Install required packages and dependencies into virtual enviornment

Install VS Code Extension for Shiny if you have not done so already.

Install required packages and dependencies. 
```zsh
pip install -r requirements.txt
```
Freeze dependencies to requirements.txt  
```zsh
python3 -m pip freeze > requirements.txt
```

### Initial Project Save
```zsh
git add .
git commit -m "initial"                         
git push origin main
```

## Run Locally - Initial Start

Create a local project virtual environment named .venv, activate it, and install the requirements.

When VS Code asks to use it for the workspace, select Yes.
If you miss the window, after installing, select from the VS Code menu, View / Command Palette, and type "Python: Select Interpreter" and select the .venv folder.

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```zsh
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip setuptools
python3 -m pip install --upgrade -r requirements.txt
```

Freeze dependencies to requirements.txt  
```zsh
python3 -m pip freeze > requirements.txt
```
Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```zsh
shiny run --reload --launch-browser dashboard/app.py
```

Open a browser to <http://127.0.0.1:8000/> and test the app.

## Run Locally - Subsequent Starts

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```zsh
python3 -m venv venv
source venv/bin/activate
shiny run --reload --launch-browser dashboard/app.py
```

## After Changes, Export to Docs Folder

Export to docs folder and test GitHub Pages locally.

Open a terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands.

```zsh
shiny static-assets remove
shinylive export dashboard docs
python3 -m http.server --directory docs --bind localhost 8009
```

Open a browser to <http://[::1]:8009/> and test the Pages app.

### Troubleshooting
Previously I got numerous error when trying to launch my app. Thanks to dilligent colleagues within the NWSU's Continuous Intelligence course, the following troubleshooting was noted. If you are running into errors running your app, it may be worth it to try downgrading websockets to version 10.4 using the following code.
```zsh
pip install websockets==10.4
```

## Push Changes back to GitHub

Open a terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands.

```zsh
git add .
git commit -m "app running"
git push -u origin main
```

## Enable GitHub Pages

Go to your GitHub repo settings and enable GitHub Pages for the docs folder.

## Explore

Implement better icons for the dashboard.

## Complete Your Project
Save your project and push back to your repository. 
```zsh
git add .
git commit -m "final"                         
git push origin main
```