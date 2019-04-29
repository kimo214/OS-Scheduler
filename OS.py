import numpy as np
import matplotlib.pyplot as plt
import time
import operator
from Tkinter import *   
import tkMessageBox
import os

class process:
    pid=0
    arrival=0
    Finish=0
    burst=0
    priority=0
    Ta=0              #TurnAorund Time
    WtTa=0            #Weighted TurnAorund Time
    remaining=0   #Remainig Time for complete execution
    running=0
    executed=0
    ready=0
    deleted=0

class scheduler:
    ready=[]
    executed=[]
    processes=0
    elapsed=0
    CS=0
    op=0
    clk=0.5
    AvgTa=0           #Average TurnAorund Time
    AvgWtTa=0         #Average Weighted TurnAorund Time
    def __init__(self,n):
        self.processes=n
    
    def switch_context(self):
        self.elapsed+=self.CS
        
        
    def update(self,t= clk):
        self.elapsed+=t
        for i in range(0,self.processes):
            if(pcb[i].running==1):
                    if(pcb[i].remaining<t): 
                            self.elapsed-=t-pcb[i].remaining
                      
                    pcb[i].remaining-=t
                    if(pcb[i].remaining<=0 or pcb[i].executed==1):
                        pcb[i].Finish=self.elapsed
                        pcb[i].running=0
                        pcb[i].executed=1
                        pcb[i].Ta=pcb[i].Finish-pcb[i].arrival
                        pcb[i].WtTa=pcb[i].Ta/pcb[i].burst
            else:
                if(pcb[i].arrival<=self.elapsed and pcb[i].executed==0):
                    if pcb[i].pid not in self.ready:
                        self.ready.append(pcb[i].pid)
                        pcb[i].ready=1

               
  
    def remove_executed(self):
        for i in range(0,self.processes):
            if(pcb[i].executed==1 and pcb[i].deleted==0):
                pcb[i].deleted=1
                self.ready.remove(pcb[i].pid)
                self.executed.append(pcb[i].pid)

    def print_values(self):
        with open("Output.txt","w") as file:
                for x in range(0,self.processes):
                    file.write("ID = "+str(x+1)+" Ta = "+str(pcb[x].Ta)+" WtTa = "+str(pcb[x].WtTa)+'\n')
                file.write("Average Turnaround = "+str(self.AvgTa)+'\n'+"Average Weighted Turnaround = "+str(self.AvgWtTa))

    def calc(self):
        for i in range(0,self.processes):
            self.AvgTa+=pcb[i].Ta
            self.AvgWtTa+=pcb[i].WtTa
        self.AvgWtTa=pcb[i].WtTa/self.processes
        self.AvgTa=pcb[i].Ta/self.processes
    

 




def generateProcess(inputFile,outputFile):
    if not os.path.exists(inputFile):
        tkMessageBox.showinfo("File Error", "Couldn't find Input File")
    
    else:
        with open(inputFile,"r") as file: 
            #first line contains number of processes
            size=int(file.readline())
            #second line contains mean and standard deviation of arrival time
            [aMean,aDev]=file.readline().split()
            aMean=float(aMean)
            aDev=float(aDev)
            #third line contains mean and standard deviation of burst time
            [bMean,bDev]=file.readline().split()
            bMean=float(bMean)
            bDev=float(bDev)
            #fouth line contains lambda of priority
            lam=float(file.readline())

        #call normal distribution function for arrival and burst times
        arrivalTimes=np.random.normal(aMean,aDev,size)
        arrivalTimes=np.abs(arrivalTimes)
        burstTimes=np.random.normal(bMean,bDev,size)
        burstTimes=np.abs(burstTimes)
        #call poisson distribution for priority
        priority= np.random.poisson(lam,size)
        priority=np.abs(priority)
        
        if outputFile=="" or outputFile.isspace():
            tkMessageBox.showinfo("File Error", "Please Enter a Valid File output name")
        else:
            with open(outputFile,"w") as file:
                file.write(str(size)+'\n')
                for x in range(size):
                    file.write(str(x+1)+" "+str(arrivalTimes[x])+" "+str(burstTimes[x])+" "+str(priority[x])+'\n')
            tkMessageBox.showinfo("Done", "Generation Successful!")

            
            
###############################################################################################################################################################


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
    
def showHome(win):
    root.deiconify()
    win.destroy()
    
    
    
def openGeneratorWin():
    processGen=Toplevel()
    processGen.geometry("500x500")
    processGen.title("Process Generator")
    root.withdraw()
    home= Button(processGen, text ="<<< Home", command = lambda: showHome(processGen))
    home.pack(fill=X)
    
    L1 = Label(processGen, text="Input File name")
    L1.pack( side = LEFT)
    F1 = Entry(processGen, bd =5)
    F1.pack(side = LEFT)
    L2 = Label(processGen, text="Output File name")
    L2.pack( side = LEFT)
    F2 = Entry(processGen, bd =5)
    F2.pack(side = LEFT)
    
    gen= Button(processGen, text ="Generate", command = lambda: generateProcess(F1.get(),F2.get()))
    gen.pack( fill=X , side = BOTTOM)

    processGen.mainloop()
    
def openSchedulerWin():
    scheduler=Toplevel()
    scheduler.geometry("500x500")
    scheduler.title("Scheduler")
    root.withdraw()
    home= Button(scheduler, text ="<<< Home", command = lambda: showHome(scheduler))
    home.pack(fill=X)
    
    frame=Frame(scheduler)
    frame.pack(fill=X,pady=10)
    L1 = Label(frame, text="Choose Algorithm")
    L1.pack( fill=X)
    
    var = IntVar()
    var.set(0)
    O1 = Radiobutton(frame, text="Non-Preemptive Highest Priority First. (HPF)", variable=var, value=1)
    O1.pack( anchor = W )

    O2 = Radiobutton(frame, text="First Come First Served. (FCFS)", variable=var, value=2)
    O2.pack( anchor = W )

    O3 = Radiobutton(frame, text="Round Robin with fixed time quantum. (RR)", variable=var, value=3)
    O3.pack( anchor = W)
    
    O4 = Radiobutton(frame, text="Preemptive Shortest Remaining Time Next. (SRTN)", variable=var, value=4)
    O4.pack( anchor = W)
    
    
    frame1=Frame(scheduler)
    frame1.pack(fill=X,pady=10)
    
    L1 = Label(frame1, text="Context Switching Time  ")
    L1.pack( side = LEFT)
    CS = Entry(frame1, bd =5)
    CS.pack(side = LEFT)
    
    frame2=Frame(scheduler)
    frame2.pack(fill=X,pady=10)
    
    L2 = Label(frame2, text="Time Quantum (If RR)  ")
    L2.pack( fill=X, side = LEFT)
    Q = Entry(frame2, bd =5)
    Q.pack(side = LEFT)
    
    frame3=Frame(scheduler)
    frame3.pack(fill=X,pady=10)
    
    L3 = Label(frame3, text="Input File ")
    L3.pack( fill=X, side = LEFT)
    F = Entry(frame3, bd =5)
    F.pack(side = LEFT)
    
    execute= Button(scheduler, text ="Execute", command = lambda: exe(var.get(),CS.get(),Q.get(),F.get()))
    execute.pack(fill=X)

    scheduler.mainloop()
    
    
def createHome():
    global root
    root = Tk()
    root.geometry("500x500")
    PG= Button(root, text ="Process Generator", command = openGeneratorWin)
    PG.pack(fill=BOTH, expand=True)
    S= Button(root, text ="Scheduler", command = openSchedulerWin)
    S.pack(fill=BOTH, expand=True)
    root.title("Home")
    root.mainloop()


###############################################################################################################################################################
    
    
     
def exe(op,CS,quantum,File):
    #checks neededd!
    if not os.path.exists(File):
        tkMessageBox.showinfo("File Error", "Couldn't find Input File")
        return
    elif op==0:
        tkMessageBox.showinfo("Op Error", "Please choose an Algorithm")
        return
    elif (quantum=="" or quantum.isspace() or not is_number(quantum) ) and op==3: #is RR
        tkMessageBox.showinfo("Op Error", "Please Enter a Number in Quantum field")
        return
    elif not is_number(CS):
        tkMessageBox.showinfo("CS Error", "Please enter a Number in Context Switch field")
        return

    with open(File,"r") as file: 
        global pcb
        size=int(file.readline())
        pcb = [process() for i in range(size)]
        ids=np.zeros(size)
        arrivals=np.zeros(size)
        bursts=np.zeros(size)
        priorities=np.zeros(size)
        for i in range(size):
            [ids[i],arrivals[i],bursts[i],priorities[i]]=file.readline().split()
            pcb[i].pid=int(ids[i])
            pcb[i].arrival=arrivals[i]
            pcb[i].burst=bursts[i]
            pcb[i].remaining=bursts[i]
            pcb[i].priority=priorities[i]

    if(op==1):
        HPF(float(CS),size)
        return
    elif(op==2):
        FCFS(float(CS),size)
        return
        
    elif(op==3):
        RR(float(CS),size,float(quantum))
        return
    
    elif(op==4):
         SRTN(float(CS),size)
         return


###############################################################################################################################################################    

#########  Algorithms ##########

def HPF(CS,size):
    sch = scheduler(size)
    sch.CS=CS
    while 1:
        if(len(sch.ready)== 0):
            sch.update() 
            continue
        else:  
            sch.update(0)

        curr=len(sch.ready)
        max_pri_pid=sch.ready[0] 
        pri=pcb[sch.ready[0]-1].priority
        for i in range(curr):
            if pcb[sch.ready[i]-1].priority>pri:
                max_pri_pid=sch.ready[i]
                pri=pcb[sch.ready[i]-1].priority    
        print(max_pri_pid)

        sch.switch_context() 

        pcb[max_pri_pid-1].running=1
        sch.update(pcb[max_pri_pid-1].burst) 

        print(sch.elapsed-pcb[max_pri_pid-1].burst,sch.elapsed)
      
        plt.bar(sch.elapsed-pcb[max_pri_pid-1].burst, max_pri_pid, width=pcb[max_pri_pid-1].burst,alpha=0.9,align='edge') 
        pcb[max_pri_pid-1].running=0
        sch.remove_executed()

        if(len(sch.executed)==size):
            break   

    sch.calc()
    sch.print_values()
    plt.show()
    return



def RR(CS,size,quantum):
    sch = scheduler(size)
    sch.CS=CS
    while 1:
        if(len(sch.ready)== 0):
            sch.update()
            continue
        else:  
            sch.update(0)
            
        print(sch.ready)

        pid=sch.ready[0]-1
        pcb[pid].running=1
        sch.switch_context()
        w= min(pcb[pid].remaining,quantum)
 
        sch.update(quantum)

        
        pcb[pid].running=0
       
        sch.ready.remove(pid+1)
        sch.ready.append(pid+1)
        

        print(pid, sch.elapsed-w,sch.elapsed)

        plt.bar(sch.elapsed-w, pid+1, width= w,alpha=0.5,linewidth=0,align='edge')

        sch.remove_executed()

        if(len(sch.executed)==size):
            break   

    sch.calc()
    sch.print_values()
    plt.show()
    return


def SRTN(CS,size):
         sch = scheduler(size)
         sch.CS=float(CS)
         while(1):
            if(len(sch.ready)==0):
                sch.update()
                continue
            working_time=0
            last_pid=-1
            crnt_pid=0
            tprocess=sch.elapsed
            while(1):
                minimum=1e10 
                for i in range(len(sch.ready)):
                    if(pcb[sch.ready[i]-1].remaining<minimum and pcb[sch.ready[i]-1].remaining>0):
                        crnt_pid=sch.ready[i]
                        minimum=pcb[sch.ready[i]-1].remaining
               

                if (last_pid==-1):
                     last_pid=crnt_pid
                     pcb[crnt_pid-1].running=1
                     working_time+=sch.clk
                     sch.update()
                     sch.remove_executed()
                     continue
               
                if(last_pid!=crnt_pid ):
                    break
                working_time+=sch.clk
                sch.update()
                sch.remove_executed()  
                if(len(sch.executed)==size or (len(sch.ready)==0)):
                    break
            
            pcb[last_pid-1].running=0
            plt.bar(tprocess, last_pid, width=working_time,alpha=0.5,align='edge')
            sch.remove_executed()
            sch.switch_context() 
            sch.update(0)
            if(len(sch.executed)==size):
                break
       
         sch.calc()
         sch.print_values()
         plt.show()
         return

def FCFS(CS,size):
        sch = scheduler(size)
        last_pid=0
        last_pos=0
        while(1):
            sch.update()
            if(len(sch.ready)==0):
                continue
            crnt_pid=sch.ready[0]
            pcb[crnt_pid-1].running=1
            if(last_pid==0):
                tprocess=pcb[crnt_pid-1].arrival
            else:
                tprocess=pcb[crnt_pid-1].arrival if (pcb[crnt_pid-1].arrival>pcb[last_pid-1].burst+last_pos+float(CS)) else pcb[last_pid-1].burst+last_pos+float(CS)
            plt.bar(tprocess, crnt_pid, width=pcb[crnt_pid-1].burst,alpha=0.5)
            plt.text(tprocess,crnt_pid+0.05,str(round(tprocess,3)),color='blue', fontweight='bold',alpha=0.8,rotation=90,va='bottom',ha='right')
            dist= ((tprocess+0.4) if pcb[crnt_pid-1].burst<0.4 else (pcb[crnt_pid-1].burst+tprocess))
            plt.text(dist,crnt_pid+0.05,str(round(dist,3)),color='blue', fontweight='bold',alpha=0.8,rotation=90,va='bottom',ha='left')
            pcb[crnt_pid-1].running=1
            sch.elapsed=tprocess+pcb[crnt_pid-1].burst
            pcb[crnt_pid-1].executed=1
            sch.update(0)
            last_pid=crnt_pid
            last_pos=tprocess
            pcb[crnt_pid-1].executed=1
            sch.remove_executed()
            if(len(sch.executed)==size):
                break
       
        sch.calc()
        sch.print_values()
        plt.show()
        return

###############################################################################################################################################################    



createHome()
        
    
