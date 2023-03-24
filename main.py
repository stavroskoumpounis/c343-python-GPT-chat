import tkinter as tk
from tkinter import ttk
from chatbot import generate_response
import threading


def get_chatbot_response(prompt):
    return generate_response(prompt, temperature)


def has_animation_tag():
    try:
        output_text.index("animation.first")
        return True
    except tk.TclError:
        return False


def update_dots_animation(counter=0):
    if waiting_for_response.get():
        dots = "." * (counter % 4)
        output_text.config(state=tk.NORMAL)
        if has_animation_tag():
            output_text.delete("animation.first", "animation.last+1c")
        output_text.insert(tk.END, f"\n\nChatbot:\nresponding{dots}\n", "animation")
        output_text.config(state=tk.DISABLED)
        counter += 1
        root.update_idletasks()
        root.after(200, update_dots_animation, counter)


def start_dots_animation():
    waiting_for_response.set(True)
    update_dots_animation()


def stop_dots_animation():
    waiting_for_response.set(False)


def get_chatbot_response_thread(prompt):
    response = get_chatbot_response(prompt)
    stop_dots_animation()
    output_text.config(state=tk.NORMAL)
    if has_animation_tag():
        output_text.delete("animation.first", "animation.last+1c")
    output_text.insert(tk.END, f"\n\nChatbot:\n{response}\n\n")
    output_text.config(state=tk.DISABLED)


def submit_prompt():
    prompt = input_text.get("1.0", tk.END).strip()
    if prompt:
        output_text.config(state=tk.NORMAL)  # Temp enable output_text
        output_text.insert(tk.END, f"You:\n{prompt}\n")
        input_text.delete("1.0", tk.END)
        root.update_idletasks()  # Force window to update immediately
        output_text.config(state=tk.DISABLED)  # Disable the output_text

        start_dots_animation()
        threading.Thread(target=get_chatbot_response_thread, args=(prompt,)).start()


root = tk.Tk()
root.title("Chatbot Interface")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

output_text = tk.Text(frame, wrap=tk.WORD, width=60, height=20, state=tk.DISABLED)
output_text.grid(row=0, column=0, columnspan=3)
output_text.tag_configure("animation")

input_text = tk.Text(frame, wrap=tk.WORD, width=40, height=4)
input_text.grid(row=1, column=0, padx=(0, 10))


def handle_return_key(event):
    if event.state & 0x4:  # if the Control key is pressed
        input_text.insert(tk.INSERT, '\n')
    else:
        submit_prompt()
    return 'break'


input_text.bind("<Return>", handle_return_key)


def set_temperature(temp_var):
    global temperature
    temperature = float(temp_var.get())


# StringVar variable to store the selected temperature value
temperature_var = tk.StringVar(value="0.5")

creative_button = tk.Radiobutton(frame, text="Creative", variable=temperature_var, value="1.0",
                                 command=lambda: set_temperature(temperature_var))
creative_button.grid(row=1, column=1)

balanced_button = tk.Radiobutton(frame, text="Balanced", variable=temperature_var, value="0.5",
                                 command=lambda: set_temperature(temperature_var))
balanced_button.grid(row=1, column=2)

precise_button = tk.Radiobutton(frame, text="Precise", variable=temperature_var, value="0.1",
                                command=lambda: set_temperature(temperature_var))
precise_button.grid(row=1, column=3)

submit_button = ttk.Button(frame, text="Submit", command=submit_prompt)
submit_button.grid(row=2, column=0, pady=(10, 0))

animation_label = ttk.Label(frame, text="")
animation_label.grid(row=2, column=1, pady=(10, 0))

temperature = 0.5  # Default temperature
waiting_for_response = tk.BooleanVar(value=False)

root.mainloop()
