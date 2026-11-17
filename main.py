import json,os,re,sys
from urllib import request as U
EU=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL not set")
V={"P":(100,2),"N":(320,18),"B":(330,14),"R":(500,4),"Q":(900,8),"K":(20000,-6)}
A1,H1,A8,H8=91,98,21,28
N,E,S,W=-10,1,10,-1
D={"P":(N,N+N,N+W,N+E),"N":(N+N+E,E+N+E,E+S+E,S+S+E,S+S+W,W+S+W,W+N+W,N+N+W),
 "B":(N+E,S+E,S+W,N+W),"R":(R0:=(N,E,S,W)),"Q":(Q0:=R0+(N+E,S+E,S+W,N+W)),"K":Q0}
T={p:tuple(v+cb*(7-abs(2*f-7)-abs(2*r-7))
 if 0<=(f:=s%10-1)<8 and 0<=(r:=s//10-2)<8 else 0 for s in range(120)) for p,(v,cb) in V.items()}
def st(b,i,c):return b[:i]+c+b[i+1:]
class C:
 def __init__(s,b,sc,wc,bc,ep,kp):s.b,s.sc,s.wc,s.bc,s.ep,s.kp=b,sc,wc,bc,ep,kp
 def moves(s):
  b=s.b
  for i,p in enumerate(b):
   if p not in "PNBRQK":continue
   for d in D[p]:
    j=i+d
    while 1:
     q=b[j]
     if q in " \nPNBRQK":break
     if p=="P":
      if d in(N,N+N) and q!=".":break
      if d==N+N and(i<A1+N or b[i+N]!="."):break
      if d in(N+W,N+E) and q=="." and j!=s.ep and abs(j-s.kp)>1:break
      if A8<=j<=H8:
       for pr in "NBRQ":yield(i,j,pr)
       break
     yield(i,j,"")
     if p in "PNK" or q in "pnbrqk":break
     if i==A1 and b[j+E]=="K" and s.wc[0]:yield(j+E,j+W,"")
     if i==H1 and b[j+W]=="K" and s.wc[1]:yield(j+W,j+E,"")
     j+=d
 def val(s,m):
  i,j,pr=m
  p,q=s.b[i],s.b[j]
  sc=T[p][j]-T[p][i]
  if q in "pnbrqk":sc+=T[q.upper()][119-j]
  if abs(j-s.kp)<2:sc+=T["K"][119-j]
  if p=="K" and abs(i-j)==2:sc+=T["R"][(i+j)//2]-T["R"][A1 if j<i else H1]
  if p=="P":
   if A8<=j<=H8:sc+=T[pr][j]-T["P"][j]
   if j==s.ep:sc+=T["P"][119-(j+S)]
  return sc
 def move(s,m):
  i,j,pr=m
  b=s.b
  wc,bc,ep,kp=s.wc,s.bc,0,0;sc=s.sc+s.val(m);p=b[i]
  b=st(b,j,p);b=st(b,i,".")
  wc=(wc[0] and i!=A1,wc[1] and i!=H1);bc=(bc[0] and j!=H8,bc[1] and j!=A8)
  if p=="K":
   wc=(False,False)
   if abs(j-i)==2:
    kp=(i+j)//2
    rf=A1 if j<i else H1
    b=st(b,rf,".");b=st(b,kp,"R")
  if p=="P":
   if A8<=j<=H8:b=st(b,j,pr)
   if j-i==2*N:ep=i+N
   if j==s.ep:b=st(b,j+S,".")
  return C(b,sc,wc,bc,ep,kp).rot()
 def rot(s):
  return C(s.b[::-1].swapcase(),-s.sc,s.bc,s.wc,119-s.ep if s.ep else 0,119-s.kp if s.kp else 0)
 def kcap(s):
  for m in s.moves():
   if s.b[m[1]]=="k" or abs(m[1]-s.kp)<2:return True
  return False
def q(p,a,b,n,c):
 n[0]+=1
 if n[0]>c or p.sc>=b:return b
 if p.sc>a:a=p.sc
 for m in sorted((m for m in p.moves() if p.b[m[1]]!="."),key=p.val,reverse=True):
  v=-q(p.move(m),-b,-a,n,c)
  if v>a:a=v
  if a>=b:break
 return a
def search(p,d,a,b,n,c):
 n[0]+=1
 if n[0]>c:return p.sc
 if d==0:return q(p,a,b,n,c)
 best=-10**9
 for m in sorted(p.moves(),key=p.val,reverse=True):
  v=-search(p.move(m),d-1,-b,-a,n,c)
  if v>best:best=v
  if best>a:a=best
  if a>=b:break
 return best
def rd(i):return chr((i-A1)%10+ord("a"))+str(1-(i-A1)//10)
def ff(fn):
 pp=fn.split()
 bd,co,ca=pp[0],pp[1],pp[2];e0=pp[3] if len(pp)>3 else "-"
 bd=re.sub(r"\d",lambda m:"."*int(m.group(0)),bd)
 b=list(21*" "+"  ".join(bd.split("/"))+21*" ")
 b[9::10]=["\n"]*12
 b="".join(b)
 wc=("Q" in ca,"K" in ca);bc=("k" in ca,"q" in ca)
 ep=(A1+ord(e0[0])-ord("a")-10*(int(e0[1])-1)) if e0!="-" else 0
 sc=sum(T[c][i] for i,c in enumerate(b) if c.isupper())
 sc-=sum(T[c.upper()][119-i] for i,c in enumerate(b) if c.islower())
 pos=C(b,sc,wc,bc,ep,0)
 return (pos,True) if co=="w" else (pos.rot(),False)
def tu(m,wp):
 i,j,pr=m
 if not wp:i,j=119-i,119-j
 return rd(i)+rd(j)+pr.lower()
def pick(fn,L):
 p,wp=ff(fn)
 lg=[m for m in p.moves() if not p.move(m).kcap()]
 if not lg:return L[0]
 lg.sort(key=p.val,reverse=True)
 best,bv=lg[0],-10**9
 for m in lg:
  v=-search(p.move(m),3,-10**9,10**9,[0],10000)
  if v>bv:bv,best=v,m
 u=tu(best,wp)
 return u if u in L else L[0]
def post(path,body):
 try:
  with U.urlopen(U.Request(EU+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})) as r:return json.load(r)
 except Exception as e:sys.exit(str(e))
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":pick(g["fen"],g["legal_moves"])})
