	PROGRAM COGORZASIM
	double precision t,a,D,R,M,V(20),g(20),tf(20),ti(20),st1,st2,dt,tabs,tesp(20),a0,t0,Cs,hsim
	double precision lata,botella,botellin,cerveza,copa,martini,vino,absenta,whisky,medio_vaso,litro,b
	integer i,tfinal,N,j
	character car*1
	
	open(unit=5,file='BAC.csv')
	write(5,'(a)')"time,in_blood_alcohol,input_alcohol"
	! tiempo inicial
	t0=0.
	! horas de simulacion
	hsim = 8.
	! tiempo final de simulacion
	tfinal=3600. * hsim
	! paso de tiempo
	dt = 1.
	
	! alcohol inicial en sangre
	a0 = 0.
	! Numero de consumiciones
	N  = 6
	
	lata = 330.
	copa = 200.
	botella = 750.
	botellin = 200.
	medio_vaso = 50.
	litro = 1000.
	
	cerveza = 0.05
	vino = 0.14
	whisky = 0.4
	hierbas = 0.3
	martini = 0.2
	absenta = 0.71
	
	! Constante de absorcion de alcohol en funcion del genero del sujeto
	hombre = 0.10
	mujer = 0.12
	
	Cabsor = hombre
	
	! Masa del sujeto
	M = 92.
	! Densidad del alcohol (g/mL)
	D = 0.789
	
	!Cs (Litros de sangre por unidad de masa del sujeto, L/kg)
	Cs=0.067
	
	! Tiempo de absorcion del alcohol (entre que se ingiere y que llega a la sangre) --> entre 15 min y 1 hora. Ponemos 20 minutos
	tabs= 20*60.
	
	!Caracteristicas de las consumiciones : v (volumen bebida) , g (graduacion) 
    !ti (tiempo de toma desde inicio simulacion), tf (tiempo en que el sujeto termina de beber)
	!tesp (tiempo de espera despues de la bebida i), tconsum (tiempo de consumo, igual a tf - ti)
	
	v(1) = lata
	g(1) = cerveza
	ti(1) = 0.
	tf(1) = 20.
	tf(1) = tf(1)*60.
	tesp(1) = 5.
	tesp(1) = tesp(1) * 60.
	
	v(2) = lata
	g(2) = cerveza
	ti(2) = tf(1)+tesp(1)
	tf(2) = tf(1)+tesp(1)+50.*60.
	tesp(2) = 15.
	tesp(2) = tesp(2) * 60.
	
	v(3) = lata
	g(3) = cerveza
	ti(3) = tf(2)+tesp(2)
	tf(3) = tf(2)+tesp(2)+30.*60.
	tesp(3) = 35.
	tesp(3) = tesp(3) * 60.

	v(4) = lata
	g(4) = cerveza
	ti(4) = tf(3)+tesp(3)
	tf(4) = tf(3)+tesp(3)+50.*60.
	tesp(4) = 15.
	tesp(4) = tesp(4) * 60.
	
	v(5) = copa
	g(5) = vino
	ti(5) = tf(4)+tesp(4)
	tf(5) = tf(4)+tesp(4)+50.*60.
	tesp(5) = 15.
	tesp(5) = tesp(5) * 60.
	
	v(6) = whisky
	g(6) = medio_vaso
	ti(6) = tf(5)+tesp(5)
	tf(6) = tf(5)+tesp(5)+10.*60.
	tesp(6) = 35.
	tesp(6) = tesp(6) * 60.
	
	a=a0
	t=t0

	
	do i=1,tfinal

		do j=1,N
			st1=1.
			st2=1.
			
			if(t-ti(j)-tabs.lt.0.) st1 = 0.
			if(t-tf(j)-tabs.lt.0.) st2 = 0.		
			a=a+D*V(j)*g(j)*Cabsor/(Cs*M*(tf(j)-ti(j)))*(st1-st2)*dt
			
			st1=1.
			st2=1.
			if(t-ti(j).lt.0.) st1 = 0.
			if(t-tf(j).lt.0.) st2 = 0.	
			b=b+D*V(j)*g(j)*Cabsor/(Cs*M*(tf(j)-ti(j)))*(st1-st2)*dt
		enddo
		
	t=t+dt
	
	if(a.le.0.) then
	a=0
	else 
	a=a-0.12/3600.*dt	
	end if 
	
	if(a.le.0.) a=0.
	
    if(mod(i,1000).eq.0)  print*, t,a,b
	if(mod(i,100).eq.0)  write(5,'(f7.2,a,f9.4,a,f9.4)')t/60,",",a,",",b
	!if(mod(i,100).eq.0)  read(*,*)
	b=0
	enddo
	
	close(5)
	
	END
