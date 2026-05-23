#modules
import math
import sympy
import sympy.parsing.sympy_parser as sparser
import tkinter as tk
from tkinter import ttk

#constants
N = 1500
P = 100

class ODESolver():
    def __init__(self,root):
        tk.Label(root, text = 'choose method', font = 'Arial 20').grid(row = 0,\
          column = 5, padx = 10, pady = 25)
        selected_method = tk.StringVar()
        combo = ttk.Combobox(root, width = 27, textvariable = selected_method)
        combo['values'] = ('Euler',
                           'Runge-Kutta(2nd order)',
                           'Runge-Kutta(4th order)')
        combo['state'] = 'readonly'
        combo.current()
        combo.grid(row = 2, column = 5)
        choice = int(input("1 for user entry, 2 for specific entry: "))
        if choice == 1:
            self.f, self.h, self.y0 = self.user_entry()
            self.user_domain_reps, self.user_domain_start = self.df(self.h)
            combo.bind("<<ComboboxSelected>>", self.callback_func_entry)
        elif choice == 2:
            self.domain_spec_start = 0 #same for all(not currently used)
            #functions
            self.f1 = "-100*y+5*(x**(3/2))*(1+40*x)"
            self.f2 = "-100*y+5*(x**(3/2))*(1+40*x)"
            self.f3 = "(0.5)*u-(1/6)*(u**3)-y"
            #steps
            self.ha = 0.0227
            self.ho = 0.020
            self.hb, self.h1, self.h2, self.h = self.ha / 2, self.ho / 2, self.ho / 4, 0.1
            self.y0 = 0
            #euler
            self.user_domain_spec_reps_ha = math.ceil(1/self.ha) + 2
            self.user_domain_spec_reps_hb = math.ceil(1 / self.hb) + 2
            #rg2
            self.user_domain_spec_reps_ho = math.ceil(1 / self.ho) + 2
            self.user_domain_spec_reps_h1 = math.ceil(1 / self.h1) + 2
            self.user_domain_spec_reps_h2 = math.ceil(1 / self.h2) + 2
            #rg4
            self.user_domain_spec_reps_h = math.ceil(40 / self.h) + 2


            self.xolist = self.x1list = self.x2list = [0]
            self.yolist = self.y1list = self.y2list = [0]

            #euler
            self.f_expr1 = sparser.parse_expr(self.f1, transformations='all')
            #rg2
            self.f_expr2 = sparser.parse_expr(self.f2, transformations='all')
            #rg4
            self.f_expr3 = sparser.parse_expr(self.f3, transformations='all')
            combo.bind("<<ComboboxSelected>>", self.callback_func_spec)


    def function(self, f_expr, x, y):
        f = self.conv(f_expr, x, y)
        print(f)
        f_val = f.evalf()
        print(f_val)
        return float(f_val)

    def user_entry(self):
        f = input("f(x) = ")
        h = float(input("h = "))
        y0 = float(input("y0 = "))
        f_expr = sparser.parse_expr(f, transformations= 'all')
        return [f_expr,h,y0]

    def conv(self, f_expr, x, y):
        fx = str(f_expr).replace('x', str(x))
        f = str(fx).replace('y', str(y))
        return sparser.parse_expr(f, transformations = 'all')

    def result_output(self, xlist, ylist):
        print("x           y")
        for i in range(self.user_domain_reps):
            print(f'{(xlist[i]):.4f}       {ylist[i]:.6f}')

    def result_output_rg4_spec(self, ylist, ulist):

        print("x           y             u")
        for i in range(self.user_domain_spec_reps_h):
            print(f'{i*0.1}               {(ylist[i]):.4f}       {ulist[i]:.6f}')

    def result_output_euler(self, xlist, ylist, step):
        print("h" + str(step) )
        print("x              y")
        if step == 0:
            for i in range(self.user_domain_spec_reps_ha):
                print(f'{(xlist[i]):.4f}       {ylist[i]:.6f}')
        elif step == 1:
            for i in range(self.user_domain_spec_reps_hb):
                print(f'{(xlist[i]):.4f}       {ylist[i]:.6f}')

    def result_output_rg2_spec(self, xlist, ylist, step):
        print("h" + str(step))
        if step == 0:
            print("x           y" + "\t" + f'\t      e[{step},{step+1}]')
        elif step == 1:
            print("x           y" + "\t" + f'\t      e[{step},{step + 1}]')
        else: print("x           y")
        if step == 0:
            for i in range(self.user_domain_spec_reps_ho):
                print(f'{(xlist[i]):.4f}       {ylist[i]:.6f}' + '     ' + str(self.control(i,step)))
        elif step == 1:
            for i in range(self.user_domain_spec_reps_h1):
                print(f'{(xlist[i]):.4f}       {ylist[i]:.6f}' + '     ' + str(self.control(i,step)))
        else:
            for i in range(self.user_domain_spec_reps_h2):
                print(f'{(xlist[i]):.4f}       {ylist[i]:.6f}' )

    def callback_func_entry(self, event):
        method = event.widget.get()
        if method == 'Euler':
            self.euler(self.f, self.h, self.y0)
        elif method == 'Runge-Kutta(2nd order)':
            self.rg2(self.f, self.h, self.y0)
        elif method == 'Runge-Kutta(4th order)':
            self.rg4(self.f, self.h, self.y0)

    def callback_func_spec(self, event):
        method = event.widget.get()
        if method == 'Euler':
            self.euler_spec(self.f_expr1, self.ha, self.y0, 0)
            self.euler_spec(self.f_expr1, self.hb, self.y0, 1)
            print("when h<h0: higher precision")
        elif method == 'Runge-Kutta(2nd order)':
            self.rg2_spec(self.f_expr1, self.ho, self.y0, 0)
            self.rg2_spec(self.f_expr1, self.h1, self.y0, 1)
            self.rg2_spec(self.f_expr1, self.h2, self.y0, 2)
            self.result_output_rg2_spec(self.xolist, self.yolist, 0)
            self.result_output_rg2_spec(self.x1list, self.y1list, 1)
            self.result_output_rg2_spec(self.x2list, self.y2list, 2)
            #self.control(1,2)
        elif method == 'Runge-Kutta(4th order)':
            self.rg4_spec(self.f_expr3)

    def euler(self, f, h, y0):
        # xm = xn + h #m->n+1
        # ym = yn + f(xn, yn) * h
        xlist = [self.user_domain_start]
        ylist = [y0]
        for i in range(N):
            xlist.append(self.user_domain_start + i*h)
            ylist.append(ylist[-1] + self.function(f, xlist[-1], ylist[-1]) * h)
        self.result_output(xlist, ylist)

    def euler_spec(self, f, h, y0, step):
        xlist = [0]
        ylist = [y0]
        for i in range(N):
            xlist.append(i*h)
            ylist.append(ylist[-1] + self.function(f, xlist[-1], ylist[-1]) * h)
        if step == 0:
            self.result_output_euler(xlist, ylist, 0)
        elif step == 1:
            self.result_output_euler(xlist, ylist, 1)

    def rg2(self, f, h, y0):
        ylist = [y0]
        xlist = [self.user_domain_start]
        for i in range(N):
            k1 = h * self.function(f, xlist[-1], ylist[-1])
            k2 = h * self.function(f, xlist[-1] + h, ylist[-1] + k1)
            xlist.append(self.user_domain_start + i * h)
            ylist.append(ylist[-1] + 0.5*(k1 + k2))
        self.result_output(xlist, ylist)

    def rg2_spec(self, f, h, y0, step):
        ylist = [y0]
        xlist = [0]
        for i in range(N):
            k1 = h * self.function(f, xlist[-1], ylist[-1])
            k2 = h * self.function(f, xlist[-1] + h, ylist[-1] + k1)
            xlist.append(i * h)
            ylist.append(ylist[-1] + 0.5 * (k1 + k2))
        if step == 0:
            self.xolist = xlist.copy()
            self.yolist = ylist.copy()
            #self.result_output_rg2_spec(xlist,ylist,0)
        elif step == 1:
            self.x1list = xlist.copy()
            self.y1list = ylist.copy()
            #self.result_output_rg2_spec(xlist,ylist,1)
        elif step == 2:
            self.x2list = xlist.copy()
            self.y2list = ylist.copy()
            #self.result_output_rg2_spec(xlist,ylist,2)


    def rg4(self, f, h, y0):
        ylist = [y0]
        xlist = [self.user_domain_start]
        for i in range(N):
            k1 = h * self.function(f, xlist[-1], ylist[-1])
            k2 = h * self.function(f, xlist[-1] + h/2, ylist[-1] + k1/2)
            k3 = h * self.function(f, xlist[-1] + h/2, ylist[-1] + k2/2)
            k4 = h * self.function(f, xlist[-1] + h, ylist[-1] + k3)
            xlist.append(self.user_domain_start + i * h)
            ylist.append(ylist[-1] + 1/6*(k1 + 2 * k2 + 2 * k3 + k4))
        self.result_output(xlist, ylist)

    def rg4_spec(self, f):
        #y(0) = 0.01, y'(0) = 0, m = 0.5
        #(1) y'' = my' - m/3(y')^3 - y = 0       f(x, y, y')
        #(2) if u->y' then u' = mu - m/3u^3 - y  f(x, y, u)

        #k1=hf(xn,yn,un)
        #k2=hf(xn+h/2,yn+k1/2,u)
        #k3=hf(xn+h/2,yn+k2/2,u)
        #k4=hf(xn+h,yn+k3,u)
        ylist = [0.01]    #x values
        ulist = [0]    #yvalues
        for i in range(N):
            k1 = self.h * self.function(f, ylist[-1], ulist[-1])
            k2 = self.h * self.function(f, ylist[-1] + self.h / 2, ulist[-1] + k1 / 2)
            k3 = self.h * self.function(f, ylist[-1] + self.h / 2, ulist[-1] + k2 / 2)
            k4 = self.h * self.function(f, ylist[-1] + self.h, ulist[-1] + k3)
            ylist.append(ylist[-1] + i * self.h)
            ulist.append(ulist[-1] + (1/6)*(k1 + 2 * k2 + 2 * k3 + k4))
        self.result_output_rg4_spec(ylist, ulist)

    def control(self,n,step):
        #we know ho>h1>h2 so we increase the position of smaller step(not the argument)
        if step == 0:
            m = math.floor(n)
            #search
            counter = 0
            while self.x1list[counter] < self.xolist[m]:
                counter += 1
            dif = self.yolist[m] - self.y1list[counter]
            if dif>0:
                abs = dif
            else: abs = -dif
            if abs<0.0005: return 0
            else: return 1
        elif step == 1:
            m = math.floor(n)
            counter = 0
            while self.x2list[counter]<self.x1list[m]:
                counter += 1
            dif = self.y1list[m] - self.y2list[counter]
            if dif>0: abs = dif
            else: abs = -dif
            if abs < 0.0005: return 0
            else: return 1



    def df(self, h):
        xst, xend = input("( , )=").split(",")
        xst = int(xst)
        d = int(xend) - int(xst)
        return [math.ceil(d / h) + 2, xst]



def main():

    root = tk.Tk()
    root.title("Methods")
    root.geometry('500x250')
    ODESolver(root)
    root.mainloop()



if __name__ == '__main__':
    main()

#-100*y+5*(x**(3/2))*(1+40*x)