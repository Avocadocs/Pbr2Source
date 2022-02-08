from tkinter import *
from tkinter import messagebox, ttk
from TkinterDnD2 import *
from pathlib import Path
from PIL import Image, ImageChops, ImageOps, ImageTk
import subprocess
import os


root = TkinterDnD.Tk()
root.title('Pbr2Source')
root.iconbitmap(r'Pbr2Source.ico')
root.geometry('300x300')
root.resizable(False, False)


tabControl = ttk.Notebook(root, takefocus=0)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Convert')
tabControl.add(tab2, text ='Settings')
tabControl.pack(expand = 1, fill ="both")


ao_list = ['ao', 'AmbiantOcclusion', 'Specular', 'specular']
roughness_list = ['rough', 'Roughness']
normal_list = ['nor', 'Normal']
list = ['_', 'base', 'albedo', 'TexturesCom', 'Metallic', 'metal', 'Height', 'Normal', 'nor', 'Roughness', 'rough', 'AmbiantOcclusion', 'occ', 'BaseColor' '256', '512', '1024', '2048']
list_base = ['base', 'albedo']


def basetexture():
    img = albedo.convert('RGB')
    img2 = occlusion.convert('RGB')
    ImageChops.multiply(img2, img).save(base_name+'_base.png')
    

def specular():
    img = occlusion.convert('RGB')
    img2 = roughness.convert('RGB')
    img2 = ImageOps.invert(img2)
    ImageChops.multiply(img, img2).save(base_name+'_specular.png')
    

def writte_vmt(base):
    os.makedirs(os.path.dirname('ExportedPBR/'+base+'.vmt'), exist_ok=True)
    with open('ExportedPBR/'+base+'.vmt', 'w') as vmt:
        vmt.write('"VertexlitGeneric"\n')
        vmt.write('{\n')
        vmt.write('	      $basetexture "'+base+'"\n')
        vmt.write('	      $surfaceprop "default"''\n')
        vmt.write('	      $bump "'+base+'_normal"\n')
        vmt.write('	      \n')
        vmt.write('	      $envmap "env_cubemap"''\n')
        vmt.write('	      $envmapmask "'+base+'_specular"\n')
        vmt.write('}')


def convert_textures(texture):
    try:
        with open("path_save.txt", "r") as f:
            g = f.read()
            f.close()
    except:
        messagebox.showerror('Error', 'Counter Strike Global Offensive path undefined !')
    vtex_path = '"'+g+'/bin/vtex" -quiet -nopause -mkdir -outdir "Exported PBR" -game "'+g+'/csgo" "'+str(os.getcwd()+'ExportedPBR/'+texture+'.tga')+'"'
    try:
        subprocess.call(vtex_path)
    except:
        messagebox.showwarning('Error', 'Error while converting .vtf')


def convert(event):
    global occlusion, roughness, albedo, base_name
    file = event.data
    base_name = Path(event.data).stem
    base = Path(event.data).stem
    for i in list:
        base_name = base_name.replace(i, '')
    for i in list_base:
        base = base.replace(i, '')
    files = []
    file_list = os.listdir(os.path.dirname(file))
    for x in file_list:
        if base in x:
            files.append(x)
    for i in files:
        if any(file in i for file in ao_list):
            occlusion = Image.open(os.path.dirname(file)+'/'+i)
        elif any(file in i for file in roughness_list):
            roughness = Image.open(os.path.dirname(file)+'/'+i)
        elif any(file in i for file in normal_list):
            normal = Image.open(os.path.dirname(file)+'/'+i)
    albedo = Image.open(event.data)
    basetexture()
    specular()
    writte_vmt(base_name)
    convert_textures(base_name)
    convert_textures(base_name+'_normal')
    convert_textures(base_name+'_specular')
    messagebox.showinfo('Info', 'Your files have been created !')


def game_config(event):
    try:
        game = event.data
    except:
        game = game_path.get()
    game_path.insert(0, game+'/')
    with open('path_save.txt', 'w') as save:
        save.write(game+'/')


#tab1
tab1.drop_target_register(DND_FILES)
tab1.dnd_bind('<<Drop>>', convert)
img = ImageTk.PhotoImage(Image.open(r'file.png').resize((100, 100)))
Label(tab1, image = img, anchor=CENTER).pack(anchor=N, pady=(40, 20))
Label(tab1, text='Drop albedo here').pack(anchor=N)


#tab 2
Label(tab2, text='Game path :').place(x=5, y=5)
game_path = ttk.Entry(tab2)
game_path.place(x=5, y=30, width=240)
game_path.drop_target_register(DND_FILES)
game_path.dnd_bind('<<Drop>>', game_config)
game_path.bind('<Return>', game_config)
ttk.Button(tab2, text='...', command=lambda:messagebox.showinfo('Game config', 'Drop game folder :\n CS:GO   Counter Strike Global Offensive\n GMOD  Garrys Mod')).place(x=260, y=29, width=30, height=23)


root.mainloop()