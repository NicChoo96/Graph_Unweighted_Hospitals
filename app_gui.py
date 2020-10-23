import json
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import fileWriteReadParser as file_parser
import algorithm_playground as algo_main


def show_two_charts(file1, file2):
    files = [file1, file2]

    root = tk.Tk()
    for i in range(0, len(files)):
        genome_size = file_parser.get_json_data(files[i])[0]['genome_length']
        df = DataFrame(file_parser.get_chart_data(files[i]), columns=['Strain_Length', 'Comparison'])
        if i == 0:
            figure = plt.Figure(figsize=(5, 4), dpi=100)
            ax = figure.add_subplot(111)
            ax.set_title("BruteForce vs FrontBack-" + str(genome_size))
            ax.set_ylim(bottom=0)
            ax.set_ylim(top=100000000)
            line = FigureCanvasTkAgg(figure, root)
            line.get_tk_widget().pack(side=tk.LEFT, expand=False)
        df = df[['Strain_Length', 'Comparison']].groupby('Strain_Length').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', marker='', fontsize=10)

    for i in range(0, len(files)):
        genome_size = file_parser.get_json_data(files[i])[0]['genome_length']
        df = DataFrame(file_parser.get_chart_data(files[i]), columns=['Strain_Length', 'Comparison'])
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.set_title(files[i] + "-" + str(genome_size))
        line = FigureCanvasTkAgg(figure, root)
        line.get_tk_widget().pack(side=tk.LEFT, expand=True)
        df = df[['Strain_Length', 'Comparison']].groupby('Strain_Length').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', marker='', fontsize=10)

    root.mainloop()


def show_single_chart(file_name):
    json_data = file_parser.get_json_data(file_name)
    if len(json_data) == 0:
        return
    genome_size = json_data[0]['genome_length']
    root = tk.Tk()
    root.title(file_name)
    df = DataFrame(file_parser.get_chart_data(file_name), columns=['Strain_Length', 'Comparison'])
    figure = plt.Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.set_title("Genome Length - " + str(genome_size))
    line = FigureCanvasTkAgg(figure, root)
    line.get_tk_widget().pack(side=tk.LEFT, expand=True)
    df = df[['Strain_Length', 'Comparison']].groupby('Strain_Length').sum()
    df.plot(kind='line', legend=True, ax=ax, color='r', marker='', fontsize=10)

    root.mainloop()


def main_gui():
    root = tk.Tk()
    root.title("Algorithm Analysis Program")
    ##############################################################################################
    # Frames

    file_frame = tk.Frame(root)
    process_algo_frame = tk.Frame(root)
    radio_frame = tk.Frame(process_algo_frame)

    scroll = tk.Scrollbar(root)

    int_var = tk.IntVar()

    text = tk.Text(root, state=tk.DISABLED, width=40)
    file_frame.pack(side=tk.LEFT)
    process_algo_frame.pack(side=tk.RIGHT)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text.pack()
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    radio_frame.pack()

    listbox = tk.Listbox(file_frame, selectmode=tk.SINGLE, width=25, height=15)

    ##############################################################################################
    # Algorithm Selector Radio Button

    tk.Label(radio_frame, text="Algorithm Selector").grid(row=0, sticky=tk.W)
    selector_radio1 = tk.Radiobutton(radio_frame, text="Brute Force", variable=int_var, value=1,
                                     command=lambda: select_algo(0))

    selector_radio1.select()
    selector_radio1.grid(row=1, sticky=tk.W)

    selector_radio2 = tk.Radiobutton(radio_frame, text="Front Back", variable=int_var, value=2,
                                     command=lambda: select_algo(1)).grid(row=2, sticky=tk.W)

    selector_radio3 = tk.Radiobutton(radio_frame, text="Boyer's Moore", variable=int_var, value=3,
                                     command=lambda: select_algo(2)).grid(row=3, sticky=tk.W)
    ##############################################################################################
    # Process Algorithm Input

    dnaStrain_label = tk.Label(process_algo_frame, text="DNA Strain")
    dnaStrain_entry = tk.Entry(process_algo_frame, bd=1)

    random_genome_length_label = tk.Label(process_algo_frame, text="Rand Genome Length")
    random_genome_length_entry = tk.Entry(process_algo_frame, bd=1)

    algo_main.text_output = text
    algo_main.root = root

    check_genome_var = tk.IntVar()
    check_genome_file = tk.Checkbutton(process_algo_frame, text="Use Genome File", variable=check_genome_var,
                                       onvalue=1, offvalue=0, height=2,
                                       width=20, command=toggle_genome)

    generate_algorithm_button = tk.Button(process_algo_frame, text="Process Algorithm",
                                          command=lambda: generate_algorithm(
                                              text, random_genome_length_entry.get(),
                                              dnaStrain_entry.get(), listbox))

    random_genome_length_label.pack()
    random_genome_length_entry.pack()
    dnaStrain_label.pack()
    dnaStrain_entry.pack()
    check_genome_file.pack()

    generate_algorithm_button.pack()

    ##############################################################################################
    # File Frame GUI - Show File and Show Charts
    file_label = tk.Label(file_frame, text="File Name")
    existing_files = file_parser.get_list_output_files()
    for i in range(0, len(existing_files)):
        listbox.insert(i, existing_files[i])

    show_file_button = tk.Button(file_frame, text="Show File", command=lambda: show_file(text, listbox))
    show_chart_button = tk.Button(file_frame, text="Show Chart",
                                  command=lambda: show_single_chart(listbox.get(tk.ANCHOR)))

    file_label.pack()
    listbox.pack()
    show_file_button.pack(side=tk.LEFT)
    show_chart_button.pack()
    ##############################################################################################
    root.mainloop()


def generate_algorithm(text, g_length, dna_strain, listbox):
    text.configure(state=tk.NORMAL)
    text.delete('1.0', tk.END)
    text.configure(state=tk.DISABLED)
    if g_length == "":
        algo_main.random_genome_length = 400000
    else:
        genome_length = int(g_length)
        if genome_length > 5000000:
            genome_length = 5000000
        algo_main.random_genome_length = genome_length
    if dna_strain == "":
        algo_main.main_test()
    else:
        algo_main.single_test_run(dna_strain)
    if not file_parser.check_output_exist():
        listbox.insert(tk.END, file_parser.file_name)


def show_file(text, listbox):
    data = file_parser.filter_file_data(listbox.get(tk.ANCHOR))
    text.configure(state=tk.NORMAL)
    text.delete('1.0', tk.END)
    text.insert(tk.END, json.dumps(data, indent=1, sort_keys=True))
    text.configure(state=tk.DISABLED)


def select_algo(selector):
    algo_main.algorithm_selector = selector


def toggle_genome():
    algo_main.use_genome_file = not algo_main.use_genome_file


main_gui()
