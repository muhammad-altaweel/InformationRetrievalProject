# import PySimpleGUI as sg                        # Part 1 - The import
#
# # Define the window's contents
#
# # Create the window
# window = sg.Window('Window Title', layout , margins=(300, 300)).read()     # Part 3 - Window Defintion
#
# # Display and interact with the Window
# event, values = window.read()                   # Part 4 - Event loop or Window.read call
#
# # Do something with the information gathered
# print('Hello', values[0], "! Thanks for trying PySimpleGUI")
#
# # Finish up by removing from the screen
# window.close()
#-------------------------------------------------------------------------------------
import PySimpleGUI as sg

layout = [  [sg.Text("Enter your Query")],     # Part 2 - The Layout
            [sg.Input()],
            [sg.Button('go')]]

# Create the window
window = sg.Window("Demo", layout,margins=(300, 300)).read()

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()