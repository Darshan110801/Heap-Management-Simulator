from tkinter import *
#globals
mem_size = 64

#Linked list utilities
class free_node:
    def __init__(self,tag,size):
        self.tag = tag
        self.size = size
        self.next = None
        self.prev = None
#initially whole memory is free
free_head = free_node(0,mem_size)

def delete_node(itr):
    global free_head
    prev_node = itr.prev
    next_node = itr.next
    if prev_node == None:
        free_head = next_node
        if free_head != None:
            free_head.prev = None
        del itr
    else:
        prev_node.next = next_node
        if next_node != None:
            next_node.prev = prev_node
        del itr

def add_to_free(tag,size):
    global free_head
    node = free_node(tag,size)
    if free_head == None:
        free_head = node
    else:
        cur = free_head
        prev = None
        while(cur != None and cur.tag<tag):
            prev = cur
            cur = cur.next
        if prev == None:
            if free_head.tag == node.tag + node.size:
                free_head.tag = node.tag
                free_head.size = free_head.size + node.size
            else:
                node.next = free_head
                free_head.prev = node
                node.prev = None
                free_head = node
        elif cur == None:
            if node.tag == prev.tag+prev.size:
                prev.size = prev.size+node.size
            else:
                prev.next = node
                node.prev = prev
                node.next = None
        else:
            if prev.tag+prev.size == node.tag and node.tag + node.size == cur.tag:
                prev.size = prev.size + node.size+cur.size
                prev.next = cur.next
                del cur
                if cur.next != None:
                    cur.next.prev = prev
            elif prev.tag+prev.size == node.tag:
                prev.size = prev.size+node.size
            elif node.tag + node.size == cur.tag:
                cur.tag = node.tag
                cur.size = cur.size+node.size
            else:
                prev.next = node
                node.prev = prev
                node.next = cur
                cur.prev = node

#Simulating alloc and dealloc
def allocate_sim(memory,tag,size,ptr_name):
    for i in range(tag,tag+size):
        memory[i].config(bg = 'black')
    memory[tag]['text'] = ptr_name
def deallocate_sim(memory,tag,size):
    memory[tag]['text'] = ''
    for i in range(tag,tag+size):
        memory[i].config(bg = 'white')

def declare_garbage(memory,ptr_name,look_up_tbl):
    for i in range(look_up_tbl[ptr_name][0],look_up_tbl[ptr_name][0]+look_up_tbl[ptr_name][1]):
        memory[i].config(bg = 'red')
    memory[look_up_tbl[ptr_name][0]]['text'] = 'GBG'

##ALLOCATING MEMORY USING FIRST FIT STRATEGY

def memory_alloc(memory,ptr_to_alloc,size,look_up_tbl,status_label):
    global free_head
    ptr_name = ptr_to_alloc.get()
    size_to_alloc = size.get()
    #flagging errors if they are present
    try:
        ptr_name = str(ptr_name)
        size_to_alloc = int(size_to_alloc)
    except:
        pass
    else:
        if(size == 0):
            status_label['text'] = "0 sized memory\ncan not be\nallocated."
        elif(len(ptr_name) == 0):
            status_label['text'] = "Variable name\ncan\'t be a\nempty string."
        elif(len(ptr_name)<=6):
            itr = free_head
            found = False
            while itr != None and (not found):
                if itr.size >= size_to_alloc:
                    found = True
                else:
                    itr = itr.next
            if found:
                if ptr_name in look_up_tbl:
                    declare_garbage(memory,ptr_name,look_up_tbl) ##if ptr_name is reassigned without freeing the
                    #memory it was already assigned with,it becomes garbage
                    del look_up_tbl[ptr_name]
                if itr.size == size_to_alloc:
                    allocate_sim(memory, itr.tag, size_to_alloc,ptr_name)
                    look_up_tbl[ptr_name] = [itr.tag,size_to_alloc]
                    delete_node(itr)
                else:
                    allocate_sim(memory,itr.tag,size_to_alloc,ptr_name)
                    look_up_tbl[ptr_name] = [itr.tag,size_to_alloc]
                    itr.size = itr.size-size_to_alloc
                    itr.tag = itr.tag + size_to_alloc
                status_label['text'] = "Status:\nMemory allocation\nsuccessful.."
            if not found:
                if ptr_name in look_up_tbl:
                    declare_garbage(memory,ptr_name,look_up_tbl) ##if ptr_name is reassigned without freeing the
                    #memory it was already assigned with,it becomes garbage
                    del look_up_tbl[ptr_name]
                status_label['text'] = "Status:\nMemory allocation\nunsuccessful.."

def memory_dealloc(memory,look_up_tbl,ptr_to_free,status_label):
    ptr = ptr_to_free.get()
    if ptr not in look_up_tbl:
        status_label['text'] = "Entered pointer\ndoes not\nexist.."
    else:
        deallocate_sim(memory,look_up_tbl[ptr][0],look_up_tbl[ptr][1])
        add_to_free(look_up_tbl[ptr][0],look_up_tbl[ptr][1])
        del look_up_tbl[ptr]
        status_label['text'] = "Status:\nMemory Deallocated\nSuccessfully.."

if __name__ == "__main__":
    root = Tk()
    root.title('Heap management with first fit strategy')
    root.configure(background = 'sky blue')
    root.geometry('600x600')
    look_up_tbl = dict()
    #for memory simulation
    memory = []
    for i in range(64):
        memory.append(Button(root,text = "",state = DISABLED,bg = 'white'))


    x_off = 0.20
    y_off = 0.30

    for i in range(8):
        for j in range(8):
            memory[i*8+j].place(relx = x_off+(1/8)*j*0.60,rely = y_off+(1/8)*i*0.60,relheight = 1/8*0.60,relwidth = 1/8*0.60)

    #for messages
    message = "**The memory is contiguous in reality.For convenience,it's shown in 2D.\n" \
              "**Names of max length 6 are only supported for pointers\n" \
              "**Enter size as positive integer only."
    message_label = Label(root,text = message,font = "Helvetica 8",bg = "sky blue")
    message_label.place(relx = 0,rely = 0.9,relheight = 0.1,relwidth = 1)
    status_label = Label(root,text = "",font = "Helvetica 10",bg = "sky blue")
    status_label.place(relx = 0.80,rely = 0.30,relwidth = 0.20,relheight = 0.60)

    #user helper grids
    back_gr = Label(root,text = '',bg = 'grey')
    back_gr.place(relx = 0,rely = 0.375,relwidth = 0.18,relheight = 0.525)
    mean = Label(root,text = "Meanings",font = "Helvetica 10 bold",bg = 'grey')
    mean.place(relx = 0,rely = 0.375,relheight = 0.075,relwidth = 0.18)
    white_button = Button(root,text ='',state = DISABLED)
    white_button.place(relx = 0.05,rely = 0.45,relwidth = 0.075,relheight = 0.075)
    white_means = Label(root,text = "Free Cell",font = "Helvetica 10 bold",bg = 'grey')
    white_means.place(relx = 0,rely = 0.525,relwidth = 0.18,relheight = 0.075)
    black_button = Button(root, text='', state=DISABLED,bg = "black")
    black_button.place(relx=0.05, rely=0.60, relwidth=0.075, relheight=0.075)
    black_means = Label(root, text="Allocated Cell", font="Helvetica 10 bold",bg = 'grey')
    black_means.place(relx=0, rely=0.675, relwidth=0.18, relheight=0.075)
    gbg_button = Button(root,text = '',bg = 'red',state = DISABLED)
    gbg_button.place(relx = 0.05,rely = 0.75,relwidth=0.075, relheight=0.075)
    gbg_label = Label(root,text = "GBG:\nGarbage cell",font = "Helvetica 10 bold",bg = "grey")
    gbg_label.place(relx = 0,rely = 0.825,relwidth = 0.18,relheight = 0.075)


    #for allocation simulation
    l_alloc = Label(root,text = "Allocate a memory",font = "Helvetica 12 bold",bg ="sky blue")
    l_alloc.place(relx = 0,rely = 0,relheight = 0.075,relwidth = 0.40)
    ptr_ask_alloc = Label(root, text="ptr name :", font="Helvetica 12 bold", bg="sky blue")
    ptr_ask_alloc.place(relx=0, rely=0.075, relheight=0.075, relwidth=0.20)
    ptr_to_alloc = Entry(root,font = "Helvetica 12 bold",justify = CENTER)
    ptr_to_alloc.place(relx = 0.20,rely = 0.075,relheight = 0.075,relwidth = 0.20)
    size_ask = Label(root, text="Size to allocate :", font="Helvetica 12 bold", bg="sky blue")
    size_ask.place(relx=0, rely=0.15,relheight=0.075, relwidth=0.20)
    size = Entry(root, font="Helvetica 12 bold", justify=CENTER)
    size.place(relx=0.20, rely=0.15, relheight=0.075, relwidth=0.20)

        #imp button
    submit_alloc = Button(root,text = "Submit",font = "Helvetica 12 bold",command = lambda : memory_alloc(memory,ptr_to_alloc,size,look_up_tbl,status_label))


    submit_alloc.place(relx = 0.20,rely = 0.225+0.0112,relheight = 0.05,relwidth = 0.20)

    #for deallocation(freeing memory) simulation

    l_free = Label(root,text = "Free the memory",font = "Helvetica 12 bold",bg = 'sky blue')
    l_free.place(relx = 0.60,rely = 0,relheight = 0.075,relwidth = 0.40)
    ptr_ask_free = Label(root,text = "ptr name :",font = "Helvetica 12 bold",bg = 'sky blue')
    ptr_ask_free.place(relx=0.60, rely=0.075, relheight=0.075, relwidth=0.20)
    ptr_to_free = Entry(root,font = "Helvetica 12 bold",justify = CENTER)
    ptr_to_free.place(relx = 0.80,rely = 0.075, relheight = 0.075,relwidth = 0.20)

    #imp button
    submit_free = Button(text = "Submit",font = "Helvetica 12 bold",command = lambda:memory_dealloc(memory,look_up_tbl,ptr_to_free,status_label))
    submit_free.place(relx = 0.80,rely = 0.15+0.0125,relheight = 0.05,relwidth = 0.20)

    root.mainloop()

