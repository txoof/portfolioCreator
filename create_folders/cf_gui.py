#!/usr/bin/env python
# coding: utf-8


# In[16]:


import logging
import PySimpleGUI as sg
import sys




# In[17]:


from rich.console import Console
from rich.markdown import Markdown




# In[18]:


#get_ipython().run_line_magic('alias', 'nb_convert ~/bin/develtools/nbconvert cf_gui.ipynb')




# In[27]:


#get_ipython().run_line_magic('nb_convert', '')




# In[37]:


def main(r=10):
    for i in range(0,r):
        print(f"{i:02}: {'*'*i}")
        pb.UpdateBar(i + 1)

        




# In[38]:


def hep():
    console = Console()
    with open("HELP.md") as readme:
        markdown = Markdown(readme.read())
        
    console.print(markdown)




# In[39]:


def text_fmt(text, *args, **kwargs): return sg.Text(text, *args, **kwargs, font='Courier 15')




layout =[ [text_fmt('Portfolio Creator')],
          [sg.Text('description\nfoo\nbar', font='Courier 11')],
          [sg.Output(size=(100, 40), font='Courier 12')],
          [sg.Text('current progress:')],
          [sg.ProgressBar(1000, orientation='h', size=(50, 20), key='progressbar')],
          [sg.Button('GO'), sg.Button('Help'), sg.Button('EXIT')],
]

window = sg.Window('Foo Window', layout=layout, keep_on_top=False)
pb = window['progressbar']
# print = sg.Print

while True:
    window.finalize()
    window.BringToFront()
    (event, value) = window.read()


    
    if event == 'EXIT' or event == sg.WIN_CLOSED:
        break
    if event == 'GO':
        main(30)
#         window.Refresh()
    if event == 'Help':
#         sg.popup_scrolled('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla faucibus bibendum pharetra. Sed ut sapien orci. Nulla tempor elementum ullamcorper. Ut turpis tellus, tempor nec placerat tristique, maximus ut magna. Morbi urna lorem, eleifend vitae risus eu, aliquet scelerisque diam. Vivamus dignissim, mauris nec rhoncus sollicitudin, neque urna molestie sapien, a pulvinar ipsum justo id lacus. Fusce neque eros, viverra eu porta non, eleifend eget massa.')
        hep()
window.close()
sg.easy_print_close()




# In[40]:


for i in range(1,10000):
    sg.one_line_progress_meter('My Meter', i+1, 10000, 'key','Optional message')




# In[ ]:


# from rich.console import Console
# from rich.markdown import Markdown

# console = Console()
# with open("README.md") as readme:
#     markdown = Markdown(readme.read())
# console.print(markdown)


