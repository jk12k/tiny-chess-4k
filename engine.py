# tiny-chess-01: 0x88 negamax, PVS + quiescence + TT + null-move + LMR, tapered PeSTO eval.
# Piece values and tables: PeSTO's evaluation function, Ronald Friederich (RofChade/PeSTO),
# as published on the Chess Programming Wiki, kept here at a sixteenth of its centipawn scale.
import json,os,sys,urllib.error,urllib.request
U=os.environ.get("MAKEFUN_ENV_URL","")
VG=(10,42,45,59,128,0)
EG=(11,35,37,64,117,0)
PH=(0,1,1,2,4,0)
D=list(map(int,"""
0 0 0 0 0 0 0 0 6 8 3 5 4 7 2 0 0 0 1 1 4 3 1 -1 0 0 0 1 1 0 1 -1 -1 0 0 0 1 0 0 -1 -1 0 0 0 0 0 2 0 -2 0 -1 -1 0 1 2 -1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 11 10 9 8 9 8 10 11 5 6 5 4 3 3 5 5 2 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
-10 -5 -2 -3 3 -6 0 -6 -4 -2 4 2 1 3 0 -1 -2 3 2 4 5 8 4 2 0 1 1 3 2 4 1 1 0 0 1 0 1 1 1 0 -1 0 0 0 1 1 1 -1 -1 -3 0 0 0 1 0 -1 -6 -1 -3 -2 -1 -1 -1 -1
-3 -2 0 -1 -1 -1 -3 -6 -1 0 -1 0 0 -1 -1 -3 -1 -1 0 0 0 0 -1 -2 -1 0 1 1 1 0 0 -1 -1 0 1 1 1 1 0 -1 -1 0 0 0 0 0 -1 -1 -2 -1 0 0 0 -1 -1 -2 -1 -3 -1 0 -1 -1 -3 -4
-1 0 -5 -2 -1 -2 0 0 -1 1 -1 0 1 3 1 -2 -1 2 2 2 2 3 2 0 0 0 1 3 2 2 0 0 0 0 0 1 2 0 0 0 0 0 0 0 0 1 1 0 0 0 1 0 0 1 2 0 -2 0 0 -1 0 0 -2 -1
0 -1 0 0 0 0 -1 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 0 0 0 0 0 -1 -1 0 -1 0 0 -1 0 -1
2 2 2 3 3 0 1 2 1 2 3 3 5 4 1 2 0 1 1 2 1 2 3 1 -1 0 0 1 1 2 0 -1 -2 -1 0 0 0 0 0 -1 -2 -1 -1 -1 0 0 0 -2 -2 -1 -1 0 0 0 0 -4 -1 0 0 1 1 0 -2 -1
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1
-4 1 1 0 -3 -2 0 0 1 0 -1 0 0 0 -2 -1 0 1 0 -1 -1 0 1 -1 -1 -1 0 -1 -1 -1 0 -2 -3 0 -1 -2 -2 -2 -2 -3 0 0 -1 -2 -2 -1 0 -1 0 0 0 -4 -2 -1 0 0 0 2 0 -3 0 -1 1 0
-4 -2 -1 -1 0 0 0 -1 0 1 0 1 1 2 1 0 0 1 1 0 1 2 2 0 0 1 1 1 1 2 1 0 -1 0 1 1 1 1 0 0 -1 0 0 1 1 1 0 0 -1 0 0 0 0 0 0 -1 -3 -2 -1 0 -1 0 -1 -2
""".split()))
NO=(33,31,18,14,-14,-18,-31,-33)
BO=(15,17,-15,-17)
RO=(1,-1,16,-16)
KO=BO+RO
CRK={0:2,7:1,112:8,119:4}
PR=(5,4,3,2)
I=1<<20
MT=1<<15
TM=[[0]*128 for _ in range(16)]
TE=[[0]*128 for _ in range(16)]
for c in range(1,15):
 t=c&7
 if 0<t<7:
  z=((t-1 if t<5 else t-2)*128) if t!=5 else -1
  for s in range(128):
   if not s&0x88:
    i=(s>>4)*8+(s&7)
    if c<8:i^=56
    TM[c][s]=VG[t-1]+(D[z+i]*2 if z>=0 else 0)
    TE[c][s]=EG[t-1]+(D[z+64+i]*2 if z>=0 else 0)
Z=[];x=88172645463325252
for _ in range(2074):x=x*6364136223846793005+1442695040888963407&0xFFFFFFFFFFFFFFFF;Z.append(x)
ZS=Z[2048]
ZC=Z[2049:2065]
B=[0]*128
T=0
C=0
E=-1
H=0
K=[4,116]
M=[0,0]
G=[0,0]
P=0
ZK=0
R={}
N=0
CP=0
AB=0
TT={}
KL=[[0,0] for _ in range(96)]
HS=[0]*16384
used=0

def sp(p,s):
 global ZK,P
 B[s]=p
 c=p>>3
 M[c]+=TM[p][s]
 G[c]+=TE[p][s]
 P+=PH[(p&7)-1]
 ZK^=Z[p*128+s]

def cp(s):
 global ZK,P
 p=B[s]
 B[s]=0
 c=p>>3
 M[c]-=TM[p][s]
 G[c]-=TE[p][s]
 P-=PH[(p&7)-1]
 ZK^=Z[p*128+s]

def mk(m):
 global T,C,E,H,ZK,K
 co=T
 f=m&255
 t=m>>8&255
 pr=m>>16
 p=B[f]
 ty=p&7
 cs=t
 ca=B[t]
 if ty==1 and t==E and not ca:
  cs=t-16+(co<<5)
  ca=B[cs]
 u=(p,ca,cs,C,E,H)
 if ca:cp(cs)
 cp(f)
 sp(pr|(co<<3) if pr else p,t)
 if ty==6:
  K[co]=t
  if t-f==2:
   cp(t+1)
   sp(4+(co<<3),t-1)
  elif f-t==2:
   cp(t-2)
   sp(4+(co<<3),t+1)
  ZK^=ZC[C]
  C&=12 if co==0 else 3
  ZK^=ZC[C]
 elif ty==4:
  d=CRK.get(f,0)
  if d:
   ZK^=ZC[C]
   C&=~d
   ZK^=ZC[C]
 if ca&7==4:
  d=CRK.get(cs,0)
  if d:
   ZK^=ZC[C]
   C&=~d
   ZK^=ZC[C]
 E=f+16 if ty==1 and t-f==32 else f-16 if ty==1 and f-t==32 else -1
 H=0 if ty==1 or ca else H+1
 T^=1
 ZK^=ZS
 R[ZK]=R.get(ZK,0)+1
 return u

def um(m,u):
 global T,C,E,H,ZK,K
 R[ZK]-=1
 if not R[ZK]:del R[ZK]
 f=m&255
 t=m>>8&255
 T^=1
 ZK^=ZS
 ZK^=ZC[C]^ZC[u[3]]
 C=u[3]
 E=u[4]
 p=u[0]
 if p&7==6:
  K[T]=f
  if t-f==2:
   cp(t-1)
   sp(p&8|4,t+1)
  elif f-t==2:
   cp(t+1)
   sp(p&8|4,t-2)
 cp(t)
 sp(p,f)
 if u[1]:sp(u[1],u[2])
 H=u[5]

def at(s,by):
 d=-16 if by==0 else 16
 for offs,pcs,sl in (((d-1,d+1),(1,),0),(NO,(2,),0),(KO,(6,),0),(BO,(3,5),1),(RO,(4,5),1)):
  for o in offs:
   n=s+o
   while not n&0x88:
    p=B[n]
    if p:
     if p>>3==by and p&7 in pcs:return 1
     break
    if not sl:break
    n+=o
 return 0

def gn(cq=0):
 ms=[]
 for s in range(128):
  if s&0x88:continue
  p=B[s]
  if not p or p>>3!=T:continue
  ty=p&7
  if ty==1:
   d=16 if T==0 else -16
   r7=7 if T==0 else 0
   n=s+d
   if not n&0x88 and not B[n]:
    if n>>4==r7:
     for q in PR:ms.append(s|n<<8|q<<16)
    elif not cq:
     ms.append(s|n<<8)
     j=n+d
     if s>>4==(1 if T==0 else 6) and not B[j]:ms.append(s|j<<8)
   for o in (d-1,d+1):
    n=s+o
    if n&0x88:continue
    q=B[n]
    if q and q>>3!=T:
     if n>>4==r7:
      for q2 in PR:ms.append(s|n<<8|q2<<16)
     else:ms.append(s|n<<8)
    elif not q and n==E:ms.append(s|n<<8)
  elif ty==6:
   for o in KO:
    n=s+o
    if n&0x88:continue
    q=B[n]
    if q:
     if q>>3!=T:ms.append(s|n<<8)
    elif not cq:ms.append(s|n<<8)
   if not cq and not at(s,T^1):
    if T==0:
     if C&1 and not B[5] and not B[6] and not at(5,1):ms.append(s|6<<8)
     if C&2 and not B[1] and not B[2] and not B[3] and not at(3,1):ms.append(s|2<<8)
    else:
     if C&4 and not B[117] and not B[118] and not at(117,0):ms.append(s|118<<8)
     if C&8 and not B[113] and not B[114] and not B[115] and not at(115,0):ms.append(s|114<<8)
  else:
   for o in (NO if ty==2 else KO if ty==5 else BO if ty==3 else RO):
    n=s+o
    while not n&0x88:
     q=B[n]
     if q:
      if q>>3!=T:ms.append(s|n<<8)
      break
     if not cq:ms.append(s|n<<8)
     if ty==2:break
     n+=o
 return ms

def ev():
 p=P if P<24 else 24
 v=((M[0]-M[1])*p+(G[0]-G[1])*(24-p))//24
 return v if T==0 else -v

def mo(m,ttm,ply):
 if m==ttm:return 1<<20
 f=m&255
 t=m>>8&255
 p=B[f]
 if m>>16:return 1<<18
 v=B[t]
 if v:return (v&7)*4096-(p&7)+(1<<17)
 if ply<96 and m in KL[ply]:return 1<<15
 return HS[f*128+t]

def qs(a,b,ply):
 global N,AB
 N+=1
 if N>=CP:
  AB=1
  return 0
 if at(K[T],T^1):ck=1;bs=-I;ms=gn()
 else:
  ck=0
  st=ev()
  if st>=b:return st
  if st>a:a=st
  bs=st;ms=gn(1)
 ms=[mo(m,0,0)<<21|m for m in ms]
 ms.sort(reverse=True)
 for x in ms:
  m=x&2097151
  u=mk(m)
  if at(K[T^1],T):
   um(m,u)
   continue
  v=-qs(-b,-a,ply+1)
  um(m,u)
  if AB:return 0
  if v>bs:
   bs=v
   if v>a:
    a=v
    if a>=b:break
 if bs==-I:bs=0 if not ck else ply-MT
 return bs

def sr(d,a,b,ply,nz):
 global N,AB,ZK,E,T
 N+=1
 if N>=CP:
  AB=1
  return 0
 if H>=100 or R.get(ZK,0)>1:return 0
 e=TT.get(ZK)
 ttm=0
 if e:
  ttm=e[3]
  if e[0]>=d:
   v=e[2]
   if v>=MT-127:v-=ply
   elif v<=127-MT:v+=ply
   if e[1]==0 or (e[1]==1 and v>=b) or (e[1]==2 and v<=a):return v
 if d<=0:return qs(a,b,ply)
 ck=at(K[T],T^1)
 if ck and ply<40:d+=1
 if nz and not ck and d>2 and P>0:
  e0=E
  E=-1
  T^=1
  ZK^=ZS
  v=-sr(d-3,-b,-b+1,ply+1,0)
  T^=1
  ZK^=ZS
  E=e0
  if AB:return 0
  if v>=b:return v
 ms=[mo(m,ttm,ply)<<21|m for m in gn()]
 ms.sort(reverse=True)
 bs=-I
 bm=ttm
 oa=a
 i=0
 for x in ms:
  m=x&2097151
  u=mk(m)
  if at(K[T^1],T):
   um(m,u)
   continue
  t=m>>8&255
  q=B[t] or m>>16 or (t==E and B[m&255]&7==1)
  if i:
   r=1+(i>5)+(i>14) if d>2 and not q and not ck and i>3 and ply>1 else 0
   v=-sr(d-1-r,-a-1,-a,ply+1,1)
   if not AB and v>a and r:v=-sr(d-1,-a-1,-a,ply+1,1)
   if not AB and a<v<b:v=-sr(d-1,-b,-a,ply+1,1)
  else:v=-sr(d-1,-b,-a,ply+1,1)
  um(m,u)
  if AB:return 0
  if v>bs:
   bs=v
   bm=m
   if v>a:
    a=v
    if a>=b:
     if not q and ply<64 and m not in KL[ply]:KL[ply]=[m,KL[ply][0]]
     break
  i+=1
 if bs==-I:bs=ply-MT if ck else 0
 if len(TT)>400000:TT.clear()
 sv=bs-ply if bs<=127-MT else bs+ply if bs>=MT-127 else bs
 if ZK not in TT or TT[ZK][0]<=d:TT[ZK]=(d,2 if bs<=oa else 1 if bs>=b else 0,sv,bm)
 return bs

def go(bd):
 global N,CP,AB,KL,HS
 N=0
 CP=bd
 AB=0
 KL=[[0,0] for _ in range(96)]
 HS=[0]*16384
 lg=[]
 for m in gn():
  u=mk(m)
  if not at(K[T^1],T):lg.append(m)
  um(m,u)
 if not lg:return 0,0,[]
 b0=lg[0]
 sc=-I
 for d in range(1,64):
  a=-I
  bm=b0
  s2=-I
  fst=1
  for m in lg:
   u=mk(m)
   if fst:v=-sr(d-1,-I,-a,1,1)
   else:
    v=-sr(d-1,-a-1,-a,1,1)
    if not AB and v>a:v=-sr(d-1,-I,-a,1,1)
   um(m,u)
   if AB:break
   if v>s2:
    s2=v
    bm=m
   if v>a:a=v
   fst=0
  if AB:break
  b0=bm
  sc=s2
  lg.remove(bm)
  lg.insert(0,bm)
 return b0,sc,lg

def bud(g,pl,tn,op):
 t=130000 if op[0]=="d" else 160000 if op=="nodes-100k" else (220000 if tn>6 else 350000)
 b=(95000000-used)//((tn-g)*60+(200-pl)//2+1)
 f=t//4
 return b if f<b<t else f if b<f else t


def uci(m):
 f=m&255
 t=m>>8&255
 pr=m>>16
 return "abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)+("nbrq"[pr-2] if pr else "")

def pmv(s):
 return "abcdefgh".index(s[0])+16*(int(s[1])-1)+(("abcdefgh".index(s[2])+16*(int(s[3])-1))<<8)+(("nbrq".index(s[4])+2)<<16 if len(s)==5 else 0)

def pos(fen,moves):
 global B,C,E,H,ZK,K,M,G,P,T,R
 B=[0]*128;M=[0,0];G=[0,0];P=0;ZK=0;R={}
 ps=fen.split();r=7;f=0
 for ch in ps[0]:
  if ch=="/":r-=1;f=0
  elif ch.isdigit():f+=int(ch)
  else:
   c="PNBRQKpnbrqk".index(ch);s=r*16+f
   sp((c%6+1)|(8 if c>5 else 0),s)
   if c%6==5:K[c//6]=s
   f+=1
 T=0 if ps[1]=="w" else 1
 H=int(ps[4])
 C=("K" in ps[2])+2*("Q" in ps[2])+4*("k" in ps[2])+8*("q" in ps[2])
 E=-1
 if ps[3]!="-":E=(int(ps[3][1])-1)*16+"abcdefgh".index(ps[3][0])
 ZK^=ZC[C]
 if T:ZK^=ZS
 R[ZK]=1
 for mv in moves:mk(pmv(mv))

def ps(path,body):
 try:
  rq=urllib.request.Request(U+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
  with urllib.request.urlopen(rq,timeout=30) as res:return json.load(res)
 except Exception as e:
  if getattr(e,"code",0)==400:return {"refused":1}
 sys.exit(1)

def main():
 global used
 if not U:sys.exit("MAKEFUN_ENV_URL is not set")
 while 1:
  g=ps("/game",{})
  if g.get("status")=="done":return
  while g.get("status")=="your_move":
   mv=g.get("moves") or []
   pos(g.get("start_fen") or g["fen"],mv)
   b,sc,order=go(bud(g.get("game") or 8,len(mv),g.get("games") or 8,g.get("opponent") or "nodes-2M"))
   used+=N
   if not b or sc<60-MT:
    ps("/resign",{"game":g["game"]})
    break
   r=ps("/move",{"game":g["game"],"move":uci(b)})
   for m in order:
    if not r.get("refused"):break
    r=ps("/move",{"game":g["game"],"move":uci(m)})
   if r.get("refused"):
    ps("/resign",{"game":g["game"]})
    break
   g=r

if __name__=="__main__":main()
