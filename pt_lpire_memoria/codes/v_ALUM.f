      subroutine vuhard(
C Read only -
     *     nblock, 
     *     jElem, kIntPt, kLayer, kSecPt, 
     *     lAnneal, stepTime, totalTime, dt, cmname,
     *     nstatev, nfieldv, nprops, 
     *     props, tempOld, tempNew, fieldOld, fieldNew,
     *     stateOld,
     *     eqps, eqpsRate,
C Write only -right click laptop touchscreen
     *     yield, dyieldDtemp, dyieldDeqps,
     *     stateNew )
C
      include 'vaba_param.inc'
C
      dimension props(nprops), tempOld(nblock), tempNew(nblock),
     1   fieldOld(nblock,nfieldv), fieldNew(nblock,nfieldv),
     2   stateOld(nblock,nstatev), eqps(nblock), eqpsRate(nblock),
     3   yield(nblock), dyieldDtemp(nblock), dyieldDeqps(nblock,2),
     4   stateNew(nblock,nstatev), jElem(nblock)
C
      character*80 cmname
      real*8 sigma0,epspl,Q1,Q2,b1,b2,C,epsdot0
      real*8 A,B,Po,n,cc,T1,DT1,T2,DT2,eq
      if (cmname(1:4).eq.'GFRP') then
C
      sigma0  = props(1)
      epspl   = props(2)
      Q1      = props(3)
      Q2      = props(4)
      b1      = props(5)
      b2      = props(6)
      C       = props(7)
      epsdot0 = props(8)
      !
      do km = 1,nblock
        if(eqpsRate(km).gt.0.0)then
         yield(km)  = sigma0+(Q1*(1-EXP(-b1*eqps(km)))+Q2*(1-EXP(-b2*eqps(km))))*(1+(eqpsRate(km)/epsdot0))**C
         dyieldDeqps(km,1) = (Q1*(b1*EXP(-b1*eqps(km)))+Q2*(b2*EXP(-b2*eqps(km))))*(1+(eqpsRate(km)/epsdot0))**C
         dyieldDeqps(km,2) = (Q1*(1-EXP(-b1*eqps(km)))+Q2*(1-EXP(-b2*eqps(km))))*(C/epsdot0)*(1+(eqpsRate(km)/epsdot0))**(C-1)
         dyieldDtemp(km) = 0.0
        else
         yield(km)  = sigma0+(Q1*(1-EXP(-b1*eqps(km)))+Q2*(1-EXP(-b2*eqps(km))))
         dyieldDeqps(km,1) = (Q1*(b1*EXP(-b1*eqps(km)))+Q2*(b2*EXP(-b2*eqps(km))))
         dyieldDeqps(km,2) = 0.0
         dyieldDtemp(km) = 0.0
      endif
      enddo
      elseif(cmname(1:4).eq.'ALUM') then
C
      A  = props(1)
      B  = props(2)
      Po = props(3)
      n  = props(4)
      cc  = props(5)
      !
      do km = 1,nblock
      plstrain=eqps(km)
      plstrnrt=eqpsRate(km)
      T1 = A+B*((plstrain)**n)
        if(plstrnrt.lt.0.000001)then
          eq = (plstrain+0.000001)**(n-1)
        else
          eq = plstrain**(n-1)
        endif      
      DT1= eq*n*B ! (n*B*((plstrain)**(n-1)))
      T2 =  (1+((plstrnrt)/Po))**cc
      DT2=  ((1+((plstrnrt)/Po))**(cc-1))*(cc)*(1/Po)
       if(plstrnrt.gt.0.0)then
        yield(km)  = T1*T2
        dyieldDeqps(km,1) = T2*DT1
        dyieldDeqps(km,2) = DT2*T1
        dyieldDtemp(km) = 0.0
       else
         yield(km)  = T1
         dyieldDeqps(km,1) = DT1
         dyieldDeqps(km,2) = 0.0
         dyieldDtemp(km) = 0.0
        endif
      enddo
      endif
C
      return
      end