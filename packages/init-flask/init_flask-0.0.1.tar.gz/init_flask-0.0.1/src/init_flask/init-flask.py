import os, subprocess, click, time, random
from urllib import request

alt_colors = ["blue", "red", "green"]

# checks for internet connection
def connected(host="https://www.google.com"):
    try:
        request.urlopen(host, timeout=15)
        return True
    except request.URLError as e:
        print(e)
        return False
    
# echoes(prints) messages to the terminal
def echo_message(message:str, showpg:bool, category='info', blink=False):
    if not showpg and category != 'error':  return      # do nothing if --showpg is off and message category isn't an error

    if category == 'info':  col = alt_colors[0]
    elif category == 'error':  col = alt_colors[1]
    else:  col = alt_colors[2]

    click.echo(click.style(message, fg=col, blink=blink))

@click.command()
@click.option('--libs', default="", help='installs comma-seperated list of libraries')
@click.option('--showpg', is_flag=True, help='show progress')
@click.option('--hardcore', is_flag=True, help='more complex initialization')
@click.argument('path')
@click.argument('project_name')
def init(showpg, libs, hardcore, path, project_name):
    t_dir = path if path != "''" else os.getcwd()
    echo_message("Initializing......", showpg, blink=True)
    time.sleep(random.randint(1, 3))  # comment out if you do not want delay
    echo_message("Creating folder......", showpg)

    # create project folder
    try:  os.mkdir(f"{t_dir}/{project_name}")
    except:
        echo_message("Invalid directory!", showpg, category='error')
        return
    
    echo_message("Folder created successfully", showpg, category='success')
    echo_message("Creating virtual environment......", showpg, blink=True)

    # create virtual environment
    venv_process = subprocess.run(["py", "-m", "venv", f"{t_dir}/{project_name}/venv"])
    if venv_process.returncode == 0:  echo_message("venv created successfully", showpg, category='success')
    else:
        echo_message("Error creating virtual environment", showpg, category='error')
        return

    # install dependencies
    if connected():
        echo_message("Installing dependencies......", showpg, blink=True)
        dependencies = ["Flask"]
        libs = libs.split(',')
        dependencies.extend(libs)   # add --libs to dependency list
        dependencies = [lib.strip() for lib in dependencies]
        command = ["pip", "install", "--target", f"{t_dir}/{project_name}/venv/lib/site-packages"]
        command.extend(dependencies)    # complete command
        install_process = subprocess.run(command)
        if install_process.returncode == 0:  echo_message("dependencies installed successfully", showpg, category='success')
        else:
            echo_message("Error installing dependencies", showpg, category='error')
            return
    else:  echo_message("No internet connection. Could not install dependencies", showpg, category='error')
    
    echo_message("Creating files......", showpg, blink=True)
    # create main file
    try:
        if hardcore:
            with open(f"{t_dir}/{project_name}/main.py", "w") as mainFile, open('../templates/main_template_hd.txt','r') as templateFile:
                mainFile.write(templateFile.read())
        else:
            with open(f"{t_dir}/{project_name}/main.py", "w") as mainFile, open('../templates/main_template.txt','r') as templateFile:
                mainFile.write(templateFile.read())
    except Exception as e:
        echo_message(f"Error creating main file;-  {e}", showpg, category='error')
        return
    
    # extras for hardcore mode
    if hardcore:
        # create all folders
        os.mkdir(f"{t_dir}/{project_name}/website")
        os.mkdir(f"{t_dir}/{project_name}/website/templates")
        os.mkdir(f"{t_dir}/{project_name}/website/models")
        os.mkdir(f"{t_dir}/{project_name}/website/static")
        os.mkdir(f"{t_dir}/{project_name}/website/static/css")

        # populate folders and files
        with open(f"{t_dir}/{project_name}/website/__init__.py", "w") as initFile, \
        open(f"{t_dir}/{project_name}/website/models/Item.py", "w") as modelFile, \
        open(f"{t_dir}/{project_name}/website/models/__init__.py", "w") as modelnitFile, \
        open(f"{t_dir}/{project_name}/website/templates/base.html", "w") as baseFile, \
        open(f"{t_dir}/{project_name}/website/static/css/style.css", "w") as cssFile, \
        open('../templates/init_template.txt','r') as initTemplateFile, \
        open('../templates/model_template.txt', 'r') as modelTemplateFile, \
        open('../templates/model_init_template.txt', 'r') as modelInitTemplateFile, \
        open('../templates/base_template.txt', 'r') as baseTemplateFile:
            initFile.write(initTemplateFile.read())
            modelFile.write(modelTemplateFile.read())
            modelnitFile.write(modelInitTemplateFile.read())
            baseFile.write(baseTemplateFile.read())
            cssFile.write('/* Styles... */')

    echo_message('Successfully initialized Flask environment🎉', showpg, category='success')

if __name__ == "__main__":
    init()