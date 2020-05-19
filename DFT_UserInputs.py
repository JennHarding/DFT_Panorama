import tkinter as tk
import DFT_Corpus as Corpus


def make_rep_input(frame, row_idx, config):
    tk.Label(frame, text="Select Repertoire:").grid(row=row_idx)
    rep_list = Corpus.full_corpus
    rep = tk.StringVar()
    rep.set(rep_list[0])
    rep_select = tk.OptionMenu(frame, rep, *rep_list)
    rep_select.grid(row=row_idx, column=1)
    rep_select.bind("<Destroy>", lambda x: config.append(('repertoire', rep.get())))    


def make_excerpt_input(frame, row_idx, config):
    measures = []
    def excerpt_box():
        if exc.get() == True:
            exc_box = tk.Toplevel()
            exc_box.title("Measure Range")

            tk.Label(exc_box, text="Begin in Measure:").grid(row=0)
            beg = tk.IntVar()
            beg_select = tk.Entry(exc_box, textvariable=beg)
            beg_select.grid(row=0, column=1)

            tk.Label(exc_box, text="End in Measure:").grid(row=1)
            end = tk.IntVar()
            end_select = tk.Entry(exc_box, textvariable=end)
            end_select.grid(row=1, column=1)  

            close_select = tk.Button(exc_box, text="Close", command=exc_box.destroy)
            close_select.grid(row=2)
            close_select.bind("<Destroy>", lambda x: measures.extend([beg.get(), end.get()]))
           
    exc = tk.BooleanVar() 
    exc_select = tk.Checkbutton(frame, text="Excerpt", variable=exc, command=excerpt_box)
    exc_select.grid(row=row_idx, sticky='w')
    exc_select.bind("<Destroy>", lambda x: config.append(('excerpt', measures)))
 

def make_win_size_input(frame, row_idx, config):
    tk.Label(frame, text="Window Size:").grid(row=row_idx, sticky='w')
    win_size = tk.IntVar()
    win_size.set(16)
    win_size_select = tk.Entry(frame, textvariable=win_size, width=2)
    win_size_select.grid(row=row_idx, column=1, sticky='w')
    win_size_select.bind("<Destroy>", lambda x: config.append(('window', win_size.get())))


def make_strategy_input(frame, row_idx, config):
    tk.Label(frame, text="PC Counting Strategy:").grid(row=row_idx, sticky='w')
    strats = ["Duration", "Onset", "Flat"]
    strat = tk.StringVar()
    strat.set(strats[0])
    strat_select = tk.OptionMenu(frame, strat, *strats)
    strat_select.grid(row=row_idx, column=1, sticky='w')
    strat_select.bind("<Destroy>", lambda x: config.append(('strategy', strat.get())))
        

def make_log_input(frame, row_idx, config):
    log = tk.BooleanVar()
    log.set(True)
    log_select = tk.Checkbutton(frame, text="Weighted Values", variable=log)
    log_select.grid(row=row_idx, sticky='w')
    log_select.bind("<Destroy>", lambda x: config.append(('log', log.get())))


def get_user_input():
    config_list = []
    ui = tk.Tk()
    ui.title("DFT User Inputs")
    
    func_list = [make_rep_input, make_excerpt_input, make_win_size_input, make_strategy_input, make_log_input]

    for idx, func in enumerate(func_list):
        func(ui, idx, config_list)
    
    tk.Button(ui, text="Done", command=ui.destroy).grid(row=len(func_list))
    ui.mainloop()

    return(dict(config_list))
