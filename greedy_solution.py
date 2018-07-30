n,s,c,h,u=[int(k) for k in raw_input().split(" ")]
import math
tl="ABCDEFGHIJ"
t=dict(zip("ABCDEFGHIJ",range(10)))
pat=[t[k] for k in raw_input()]
bb=[t[k] for k in raw_input()]


tn=[[] for i in range(10)]
for i in range(n):
    tn[pat[i]]+=[i]


nexti=[[None for j in range(n)] for i in range(10)]
for i in range(10):
    for j in range(len(tn[i])):
        nxt=tn[i][(j+1)%len(tn[i])]
        if j==len(tn[i])-1:
            for k in range(nxt)+range(tn[i][j],n):
                nexti[i][k]=nxt
        else:
            for k in range(tn[i][j],nxt):
                nexti[i][k]=nxt

maxres=0
mf=0
for fact in [0.1,0.25,0.5,1.0,1.5,2.0,3.0,5.0,10.0]:
    z=range(10)
    zm=z[:]
    bot=bb[:]
    def findnext(wfrom,color):
        wfo=wfrom
        while  (nexti[color][wfrom%n]-wfrom)%n+wfrom in z:
            wfrom+=(nexti[color][wfrom%n]-wfrom)%n
        return (nexti[color][wfrom%n]-wfrom)%n+wfrom

    m=[[None for i in range(10)] for j in range(10)]
    for i in range(10):
        for col in range(10):
            nxt=findnext(z[i],col)
            m[i][col]=nxt-z[i]

    mz=max(z)
    mnz=min(z)
    def margmax(poss=range(10),typ=1):
        mx=-10000000
        res=None
        for i in range(10):
            for j in poss:
                vtc=m[i][j]*((float(mz-z[i])/(mz-mnz))**typ)
                if vtc>mx:
                    res=(i,j)
                    mx=vtc
        return res

    rr=[]
    kk=0
    while kk<s:
        kk+=1
        best=margmax(list(set(bot[:h])),typ=fact)
        bg=best[0]
        rr+=[best]
        i=best[1]
       # print h,len(bot)
        for k in range(h):
            if i==bot[k]:
                bot=bot[:k]+bot[k+1:]
                break
        ctc=[i,pat[z[bg]%n]]
        oz=z[bg]
        z[bg]+=m[bg][i]
        tp=m[bg][i]
        for c in ctc:
            for j in range(10):
                if j!=bg:
                    m[j][c]=findnext(z[j],c)-z[j]
        for col in range(10):
            m[bg][col]=findnext(z[bg],col)-z[bg]
        mz=max(z)
        mnz=min(z)
       # print best[0],tl[best[1]]#,tp
    #print fact,z,min(z)
    if min(z)>maxres:
        maxres=min(z)
        mf=fact
    

#print mf
#1/0
for fact in [mf]:
    z=range(10)
    zm=z[:]
    bot=bb[:]
    def findnext(wfrom,color):
        wfo=wfrom
        while  (nexti[color][wfrom%n]-wfrom)%n+wfrom in z:
            wfrom+=(nexti[color][wfrom%n]-wfrom)%n
        return (nexti[color][wfrom%n]-wfrom)%n+wfrom

    m=[[None for i in range(10)] for j in range(10)]
    for i in range(10):
        for col in range(10):
            nxt=findnext(z[i],col)
            m[i][col]=nxt-z[i]

    mz=max(z)
    mnz=min(z)
    def margmax(poss=range(10),typ=1):
        mx=-10000000
        res=None
        for i in range(10):
            for j in poss:
                vtc=m[i][j]*((float(mz-z[i])/(mz-mnz))**typ)
                if vtc>mx:
                    res=(i,j)
                    mx=vtc
        return res

    rr=[]
    kk=0
    while kk<s:
        kk+=1
        best=margmax(list(set(bot[:h])),typ=fact)
        bg=best[0]
        rr+=[best]
        i=best[1]
       # print h,len(bot)
        for k in range(h):
            if i==bot[k]:
                bot=bot[:k]+bot[k+1:]
                break
        ctc=[i,pat[z[bg]%n]]
        oz=z[bg]
        z[bg]+=m[bg][i]
        tp=m[bg][i]
        for c in ctc:
            for j in range(10):
                if j!=bg:
                    m[j][c]=findnext(z[j],c)-z[j]
        for col in range(10):
            m[bg][col]=findnext(z[bg],col)-z[bg]
        mz=max(z)
        mnz=min(z)
        print best[0],tl[best[1]]#,tp
    #print fact,z,min(z)
    #if min(z)>maxres:
    #    maxres=min(z)
    #    mf=fact