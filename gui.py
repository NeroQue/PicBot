import tkinter as tk
# from discord_bot import bot


def send_image():
    # Get the selected server and channel from the GUI elements
    selected_server = server_dropdown.get()
    selected_channel = channel_dropdown.get()

    # Get the service and search query from the input fields
    selected_service = service_entry.get()
    search_query = query_entry.get()

    # Formulate the command based on the selected service and search query
    command = f'/{selected_service} {search_query}'

    # Get the Discord channel object
    channel = bot.get_channel(selected_channel)

    # Send the command to the selected channel in the selected server
    bot.dispatch('message', channel, command)

def create_gui():
    root = tk.Tk()
    root.title("Discord Bot GUI")

    # Create and place widgets (text boxes, dropdown, buttons) in the window
    service_label = tk.Label(root, text="Service:")
    service_label.pack()
    service_entry = tk.Entry(root)
    service_entry.pack()

    tag_label = tk.Label(root, text="Tag:")
    tag_label.pack()
    tag_entry = tk.Entry(root)
    tag_entry.pack()

    # Create dropdown for channels
    channels = ['channel1', 'channel2', 'channel3']  # Replace with actual channel names
    channel_dropdown = tk.StringVar(root)
    channel_dropdown.set(channels[0])
    channel_menu = tk.OptionMenu(root, channel_dropdown, *channels)
    channel_menu.pack()

    send_button = tk.Button(root, text="Send Image", command=send_image)
    send_button.pack()

    root.mainloop()
