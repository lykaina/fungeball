'''
Fungeball Interpreter v1.0-beta4 Library

Copyright (c) 2025 Sara Berman

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
'''

class Fungeball:
    def __init__(self,fname,xmax=80,ymax=25):
        from sys import stdin, stdout
        self.fname=fname
        self.xmax=xmax
        self.ymax=ymax
        self.stack=[0,0,0]
        self.xdir=1
        self.ydir=0
        self.xpos=0
        self.ypos=0
        self.smode=False
        self.grid=[]
        self.ibuf=b''
        self.obuf=b''
        self.threads=1
        self.tstacks=[[0,0,0]]
        self.tdelta=[[1,0]]
        self.tpos=[[0,0]]
        self.tsmode=[[0]]
        self.tnew=False
        self.stdin=stdin
        self.stdout=stdout
    def buf_in(self):
        _in=self.stdin.read(1)
        if _in == None or _in == '':
            pass
        else:
            self.ibuf=self.ibuf+_in.encode()
    def buf_in_pop(self):
        _r=self.ibuf[0]
        if len(self.ibuf) > 1:
            self.ibuf=self.ibuf[1:]
        else:
            self.ibuf=b''
        #if _r == 13:
        #    _r = 10
        #else:
        #    pass
        return _r
    def buf_in_get(self):
        while self.ibuf == b'':
            self.buf_in()
    def buf_out(self):
        while len(self.obuf) > 1:
            self.stdout.write(chr(self.obuf[0]))
            self.obuf=self.obuf[1:]
        if len(self.obuf) == 1:
            self.stdout.write(chr(self.obuf[0]))
            self.obuf=b''
    def buf_out_put(self,chin):
        if chin.encode() == b'\n':
            self.obuf=self.obuf+b'\n'
        else:
            self.obuf=self.obuf+chin.encode()
    def make_grid(self):
        befile = open(self.fname,'rb')
        befile_lst = befile.readlines()
        befile.close()
        del befile
        flst = []
        flsts = []
        i=0
        for i in range(len(befile_lst)):
            flst.append(befile_lst[i].strip(b'\n').strip(b'\r'))
            flsts.append(len(flst[i][0:self.xmax]))
        del befile_lst
        xi=0
        yi=0
        gt=[]
        for yi in range(len(flsts)):
            lt=[]
            for xi in range(flsts[yi]):
                lt.append((flst[yi][xi]).to_bytes())
            gt.append(lt)
            del lt
        del flst
        del flsts
        grid=[]
        ym=0
        if len(gt) <= self.ymax:
            ym=len(gt)
        else:
            ym=self.ymax
        xi=0
        yi=0
        for yi in range(ym):
            lt=[]
            for xi in range(len(gt[yi])):
                lt.append(gt[yi][xi])
            if len(gt[yi]) < self.xmax:
                for xi in range(self.xmax-len(gt[yi])):
                    lt.append(b' ')
            grid.append(lt)
            del lt
        ym=self.ymax-ym
        if ym > 0:
            for yi in range(ym):
                lt=[]
                for xi in range(self.xmax):
                    lt.append(b' ')
                grid.append(lt)
                del lt
        else:
            pass
        self.grid=grid
        del grid
    def edit_grid(self,xc=0,yc=0,c=b' '):
        ngrid=[]
        xi=0
        yi=0
        for yi in range(yc):
            ngrid.append(self.grid[yi])
        lt=[]
        for xi in range(xc):
            lt.append(self.grid[yc][xi])
        lt.append(c)
        for xi in range(self.xmax - (xc+1)):
            lt.append(self.grid[yc][xc+xi+1])
        ngrid.append(lt)
        for yi in range(self.ymax - (yc+1)):
            ngrid.append(self.grid[yc+yi+1])
        self.grid=ngrid
    def move_pc(self):
        self.xpos=(self.xmax+self.xpos+self.xdir)%self.xmax
        self.ypos=(self.ymax+self.ypos+self.ydir)%self.ymax
    def run_char(self,gch=b' '):
        from random import seed,randint
        from time import time_ns
        from math import floor,log10
        ret=0
        if len(self.stack) == 0:
            self.stack=[0,0,0]
        elif len(self.stack) == 1:
            self.stack=[0,0,self.stack[0]]
        elif len(self.stack) == 2:
            self.stack=[0,self.stack[0],self.stack[1]]
        else:
            pass
        if self.smode == False:
            if gch == b' ':
                pass
            elif gch == b'+':
                b=self.stack.pop()
                a=self.stack.pop()
                self.stack.append(a+b)
            elif gch == b'-':
                b=self.stack.pop()
                a=self.stack.pop()
                self.stack.append(a-b)
            elif gch == b'*':
                b=self.stack.pop()
                a=self.stack.pop()
                self.stack.append(a*b)
            elif gch == b'/':
                b=self.stack.pop()
                a=self.stack.pop()
                self.stack.append(a//b)
            elif gch == b'%':
                b=self.stack.pop()
                a=self.stack.pop()
                self.stack.append(a%b)
            elif gch == b'!':
                a=self.stack.pop()
                if a != 0:
                    self.stack.append(0)
                else:
                    self.stack.append(1)
            elif gch == b'`':
                b=self.stack.pop()
                a=self.stack.pop()
                if a > b:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            elif gch == b'>':
                self.xdir=1
                self.ydir=0
            elif gch == b'<':
                self.xdir=-1
                self.ydir=0
            elif gch == b'^':
                self.xdir=0
                self.ydir=-1
            elif gch == b'v':
                self.xdir=0
                self.ydir=1
            elif gch == b'?':
                seed(time_ns())
                r=randint(0,3)
                if r == 0:
                    self.xdir=0
                    self.ydir=-1
                elif r == 1:
                    self.xdir=1
                    self.ydir=0
                elif r == 2:
                    self.xdir=0
                    self.ydir=1
                elif r == 3:
                    self.xdir=-1
                    self.ydir=0
                else:
                    pass
            elif gch == b'_':
                a=self.stack.pop()
                if a != 0:
                    self.xdir=-1
                    self.ydir=0
                else:
                    self.xdir=1
                    self.ydir=0
            elif gch == b'|':
                a=self.stack.pop()
                if a != 0:
                    self.xdir=0
                    self.ydir=-1
                else:
                    self.xdir=0
                    self.ydir=1
            elif gch == b'"':
                self.smode=True
            elif gch == b':':
                a=self.stack.pop()
                self.stack.append(a)
                self.stack.append(a)
            elif gch == b'\\':
                b=self.stack.pop()
                a=self.stack.pop()
                self.stack.append(b)
                self.stack.append(a)
            elif gch == b'$':
                a=self.stack.pop()
            elif gch == b'.':
                a=self.stack.pop()
                i=0
                l=0
                s=0
                o=''
                if a != 0:
                    l=floor(log10(abs(a)))
                    s=a//abs(a)
                else:
                    l=0
                    s=1
                if s == -1:
                    o=o+'-'
                else:
                    pass
                for i in range(l+1):
                    o=o+chr(48+(abs(a)//pow(10,l-i))%10)
                o=o+' '
                self.buf_out_put(o)
            elif gch == b',':
                a=self.stack.pop()
                o=chr(abs(a))
                self.buf_out_put(o)
            elif gch == b'#':
                self.move_pc()
            elif gch == b'g':
                b=self.stack.pop()
                a=self.stack.pop()
                self.stack.append((self.grid[b%self.ymax][a%self.xmax])[0])
            elif gch == b'p':
                b=self.stack.pop()
                a=self.stack.pop()
                v=self.stack.pop()
                self.edit_grid(a%self.xmax,b%self.ymax,chr(v).encode())
            elif gch == b'&':
                a=0
                b=0
                d=[]
                self.buf_in_get()
                a=self.buf_in_pop()
                while a < 48 or a > 57:
                    d.append(a)
                    self.buf_in_get()
                    a=self.buf_in_pop()
                while a >= 48 and a <= 57:
                    b=b*10+(a-48)
                    self.buf_in_get()
                    a=self.buf_in_pop()
                self.stack.append(b)
            elif gch == b'~':
                self.buf_in_get()
                a=self.buf_in_pop()
                self.stack.append(a)
            elif gch == b'@':
                ret=1
            elif gch == b'0':
                self.stack.append(0)
            elif gch == b'1':
                self.stack.append(1)
            elif gch == b'2':
                self.stack.append(2)
            elif gch == b'3':
                self.stack.append(3)
            elif gch == b'4':
                self.stack.append(4)
            elif gch == b'5':
                self.stack.append(5)
            elif gch == b'6':
                self.stack.append(6)
            elif gch == b'7':
                self.stack.append(7)
            elif gch == b'8':
                self.stack.append(8)
            elif gch == b'9':
                self.stack.append(9)
            elif gch == b'n':
                self.stack=[0,0,0]
            elif gch == b'q':
                a=self.stack.pop()
                ret=a+2
            elif gch == b't':
                self.tnew=True
            elif gch == b'z':
                pass
            else:
                self.xdir=self.xdir*-1
                self.ydir=self.ydir*-1
        else:
            if gch == b'"':
                self.smode=False
            else:
                self.stack.append(gch[0])
        return ret
    def run_thread(self):
        tr=0
        cmdch = self.grid[self.ypos][self.xpos]
        while cmdch == b' ' and self.smode == False:
            self.move_pc()
            cmdch = self.grid[self.ypos][self.xpos]
        tr=self.run_char(cmdch)
        self.buf_out()
        return tr
    def run_grid(self):
        trun=0
        while trun == 0 and self.threads > 0:
            ti=0
            tn=self.threads
            ts=[]
            tsm=[]
            tp=[]
            td=[]
            new_t=[]
            self.stack=[]
            for ti in range(self.threads):
                run=0
                self.stack=self.tstacks[ti]
                self.xpos=self.tpos[ti][0]
                self.ypos=self.tpos[ti][1]
                self.xdir=self.tdelta[ti][0]
                self.ydir=self.tdelta[ti][1]
                if self.tsmode[ti][0] == 0:
                    self.smode=False
                else:
                    self.smode=True
                run=self.run_thread()
                if run < 0 or run > 1:
                    trun=run-2
                elif run == 1:
                    tn=tn-1
                else:
                    if self.tnew == False:
                        pass
                    else:
                        tn=tn+1
                        new_t.append([[],[(self.xmax + self.xpos - self.xdir) % self.xmax,(self.ymax + self.ypos - self.ydir) % self.ymax],[self.xdir*-1,self.ydir*-1],[0]])
                        for si in range(len(self.stack)):
                            new_t[0].append(self.stack[si])
                        self.tnew=False
                    self.move_pc()
                    ts.append(self.stack)
                    tp.append([self.xpos,self.ypos])
                    td.append([self.xdir,self.ydir])
                    if self.smode == False:
                        tsm.append([0])
                    else:
                        tsm.append([1])
                self.stack=[]
            if len(new_t) > 0:
                i=0
                for i in range(len(new_t)):
                    ts.append(new_t[i][0])
                    tp.append(new_t[i][1])
                    td.append(new_t[i][2])
                    tsm.append(new_t[i][3])
            else:
                pass
            #print('{',tn,ts,tp,td,tsm,'}')
            self.tstacks=ts
            self.tpos=tp
            self.tdelta=td
            self.tsmode=tsm
            self.threads=tn
        return trun

def main(file,xmax=80,ymax=25):
    import gc
    from sys import exit as sys_exit
    bft=Fungeball(file,xmax,ymax)
    bft.make_grid()
    gc.collect()
    rv=bft.run_grid()
    del bft
    gc.collect()
    if rv != 0:
        sys_exit(abs(rv)%256)
