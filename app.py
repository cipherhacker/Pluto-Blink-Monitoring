#!/bin/python
"""
Hello World, but with more meat.
"""

import wx
import os
import sys
import subprocess
from wx.adv import Animation, AnimationCtrl

import time
from time import sleep




class HelloFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)
        pnl = wx.Panel(self)
        pnl.SetBackgroundColour('black')
        self.CreateStatusBar()
        self.SetStatusText("Created by team Alphabreak.")
        self.btn = wx.Button(pnl, -1, "Start Streaming")
        self.btn.Bind(wx.EVT_BUTTON, self.onClicked)
        self.btn.SetPosition((130,180))
        self.initialize(pnl)
        
        self.btn2 = wx.Button(pnl, -1, "Analyze my data")
        self.btn2.Bind(wx.EVT_BUTTON, self.onClicked2)
        self.btn2.SetPosition((125,300))
        self.initialize(pnl)

        self.btn3 = wx.Button(pnl, -1, "Stop Streaming")
        self.btn3.Bind(wx.EVT_BUTTON, self.onClicked3)
        self.btn3.SetPosition((130,240))
        self.initialize(pnl)



    def initialize(self, pnl):
        self.st = wx.StaticText(self, label="Pluto: Blink monitoring", pos=(25,25))
        self.st.SetPosition((50,50))
        self.st.SetForegroundColour('white')
        self.st.SetBackgroundColour('black')
        font = self.st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.st.SetFont(font)
        print("Initiating environment for run...")
        self.SetStatusText("Initiating environment for run...")




    def makeMenuBar(self):

        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def onClicked(self, event):
        btn = event.GetEventObject().GetLabel()
        print("Button clicked: ",btn)
        print("Starting background services...")
        self.SetStatusText("Starting background services...")
        fileInstance = open('shared_output.txt', 'w')
        fileInstance.write("{}".format(0))
        self.process_detection = subprocess.Popen([sys.executable, 'detect_blinks.py'])
        self.process_tkinter_window = subprocess.Popen([sys.executable, 'tk.py'])


    def onClicked2(self, event):
        self.process_visual = subprocess.Popen([sys.executable, 'plt.py'])
        print('Generating graphical analysis...')
        self.SetStatusText("Generating graphical analysis...")

    def onClicked3(self, event):
        self.process_detection.terminate()
        print('Initiating process termination...')
        self.SetStatusText("Initiating process termination...")
        self.process_tkinter_window.terminate()

    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hey")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a blink counting system created by team Alphabreak.",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App(False)
    frm = HelloFrame(None, title='Pluto by Alphabreak')
    frm.Show()
    app.MainLoop()