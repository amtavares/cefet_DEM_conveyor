#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define iA 843314861
#define iB 453816693
#define iM 1073741824
#define graosMax 10000

FILE *f1;
FILE *f2;

int restnum; //caso queira iniciar a simulação a partir de uma outra configuração já feita no depose
char nnq[2], narq[3], datname[16], nom[3], datnameaux1[12], datnameaux2[12];
int nq, npa, npap, iaff, ifreqv, isauve, irep, nball, nl, ntotal, ncont, icont0, igliss, itaux;
static int ior[5*graosMax], iex[5*graosMax], io[5*graosMax], liste[2][5*graosMax], nnvois[5*graosMax];
static float r[2][graosMax], xr[graosMax], ivmass[graosMax], ivmominit[graosMax], v[2][graosMax], a[2][graosMax], rot1[graosMax], rot2[graosMax], rot3[graosMax];
static float rp[2][graosMax], vp[2][graosMax], ap[2][graosMax], rot1p[graosMax], rot2p[graosMax], rot3p[graosMax];
static float eij[5*graosMax], xnij[2][5*graosMax], reacn[5*graosMax], react[5*graosMax], react0[5*graosMax], fp[2][5*graosMax], Gamma[graosMax];
float kn, ks, frott, frot2, dt, dt2s2, c1, xray, cofkn, zmass, ivmasstot, xrmax, xrmin, dhr, xrand, gn;

void init();
void putball();
void sauveconf(int num);
void recherche_voisins1();
void predicteur();
void detectcontacts();
void calculforces();
void archivagereaction();
void correcteur();
void verifequilibre();
void affichage();
//int signe(float val1, float val2);
//void CundallDamping();



int isem;
isem=678912345;
//isem=645897312;
//isem=469882347;
//isem=789123565;
//isem=032569874;

float rand0() 
{
      float aux, x;
      aux = 0.5/iM;
      isem = isem*iA + iB;
      if (isem<0) isem = (isem+ iM) + iM; 
      x=isem*aux;      
      return x;           
}

void SystemPause()
{
   char magickey;
   fflush(stdin);
   printf("\n\n Appuyez sur une touche pour continuer...");
   scanf("%c", &magickey);
   magickey = getc(stdin);
}

int main()
{
    int it;
    init(); //esta função ainda falta ler as forças iniciais      
    nball=0;
    putball();
    recherche_voisins1(); //conferida
    it=0; 
    itaux=0;
    int contsauve;
    contsauve = restnum;
    sauveconf(contsauve);
    while(nball<=irep) //condição somente para rodar o programa, dps isto será trocado
    {
             it++;
             if ( (it % 5000) == 0 )
             {
                  itaux=it/5000;
                  if ( (itaux % 2) == 0 ) //tempo de relaxação
                  {
                        printf("\n\n  Esferas colocadas = %d.", nball);
                       // if((itaux % 20) == 0) { 
			     contsauve++;
			     sauveconf(contsauve);
			//}
                        putball();
                        recherche_voisins1();
                  }
             }
             if ( (it % ifreqv) == 0 ) recherche_voisins1();
             predicteur();   //particula cresce de tamanho aqui
             detectcontacts();
             calculforces();
             archivagereaction();
             //CundallDamping();
             correcteur();
             /*if ( (it % iaff) == 0) 
             {
                  verifequilibre();
                  affichage();
             }*/
    }
    printf("\n Simulação finalizada!");
    SystemPause();
}

void init()
{
         char lecforces;
         int i, j, iq1, iq2, ill, il;
         int ab, b, c, d, e, f; 
                  
         printf("\n  Digite o valor de nq: ");
         scanf("%d", &nq);
         printf("\n  Digite a configuracao de inicio (todos os caracteres): "); //printf("\n  Digite a configuracao de inicio (tres letras): ");
         scanf("%s", &datnameaux1); //scanf("%s", &narq);

         int num;
         
         printf("\n  Digite a configuracao a ser guardada (todos os caracteres): "); //printf("\n  Digite a configuracao a ser guardada (tres letras): ");
         scanf("%s", &datnameaux2); //scanf("%s", &nom);
         //printf("\n  Digite os valores de kn: "); //constante de mola na direção normal
         //scanf("%f", &kn); 
         //printf("\n  Digite o valor de ks: "); //constante de mola na direção tangencial
         //scanf("%f", &ks);
         printf("\n  Digite o coeficiente de atrito (particula-particula): ");
         scanf("%f", &frott);
         printf("\n  Digite o coeficiente de atrito (particula-meio): ");
         scanf("%f", &frot2);/*
         printf("\n  A frequencia de exibicao eh: ");
         scanf("%d", &iaff);
         printf("\n  O valor da frequencia calculada dos vizinhos: ");
         scanf("%d", &ifreqv);
         printf("\n  Qual a frequencia de verificacao do equilibrio: ");
         scanf("%d", &isauve);
*/
kn=1000; ks = kn; iaff=1000;ifreqv=100;isauve=1000; 
//frott=0.5; 
//frot2=0.15;

         do
         {
                 printf("\n  Realizar leitura das forcas iniciais? (S/N): ");
		 scanf("%c", &lecforces);                  
         }while( (lecforces != 'S') && (lecforces != 's') && (lecforces != 'N') && (lecforces != 'n') );
         
         if ( (lecforces == 'N') || (lecforces == 'n') ) { sprintf(datname, "%s.dat", datnameaux1); restnum = 0;} 
	 else
	 {
	 	printf("\n\n  Digite o numero da configuracao: ");
	 	scanf("%d", &restnum);
	 	sprintf(datname, "%s_%04d.txt", datnameaux1,  restnum); 
	 } 		  
         printf("\n\n  O nome do seu arquivo que ira abrir eh %s\n", datname);
	 SystemPause();
         

	 f1=fopen(datname, "r");
         fscanf(f1,"%d %d\n", &npa, &npap);
         if ( (lecforces == 'N') || (lecforces == 'n') ) for(i=0; i<npap; i++) fscanf(f1, "%f %f %f\n", &r[0][i], &r[1][i], &xr[i]); //conf do prepare
         else if( (lecforces == 'S') || (lecforces == 's') ) //haverá leitura das forças (pois utilizou-se uma conf originada do depose)
         {
               for(i=0; i<npap; i++) fscanf(f1, "%f %f %f %f %f\n", &r[0][i], &r[1][i], &xr[i], &ivmass[i], &ivmominit[i]);
               fscanf(f1, "%f %f %f %f %f %f\n", &ab, &b, &c, &d, &e, &f); 
               fscanf(f1, "%d %d\n", &ncont, &ntotal);
               for(ill=1; ill<=ntotal; ill++)
               {
                      fscanf(f1, "%d %d %d %f %f %f %f\n", &il, &i, &j, &reacn[ill], &react0[ill], &xnij[0][ill], &xnij[1][ill]); 
                      ior[ill]=i-1;
                      iex[ill]=j-1;
		      io[ill]=0;
               }
               printf("\n  Digite o numero de partículas da base (npa): ");
               scanf("%d", &npa);
	       SystemPause();
         }
         fclose(f1);
       
         //printf("\n\n npa=%d, npap=%d", npa, npap); //tirar
         //for(i=0; i<npap; i++) printf("\n posicao x=%f, posicao y=%f, raio=%f", r[0][i], r[1][i], xr[i]); //tirar
         //printf("\n\n  "); //tirar dps
	 //SystemPause();
         
	 //calculo para saber inverso da massa total
         zmass=0.0;
         ivmasstot=0.0;
	 xrmax=0.0;
         for(i=0; i<npap; i++) if(xr[i]>xrmax) xrmax=xr[i];

         printf("\n  xrmax=%f \n", xrmax);
         for(i=0; i<npap; i++) 
         {
               ivmass[i] = (xrmax*xrmax)/(xr[i]*xr[i]); //inverso da massa normalizada
               ivmominit[i] = 2.0*ivmass[i]/(xr[i]*xr[i]); //inverso do momento de inercia/ MI disco=(m*r^2)/2 (neste caso, normalizado)
               if (ivmass[i]>zmass) zmass=ivmass[i]; /*menor massa resultara em maior ivmass[i]*/
               ivmasstot = ivmasstot + 1.0/ivmass[i];      
         }
         ivmasstot = 1.0/ivmasstot; //inverso da massa total
         //printf ("\n  A menor massa eh %f.", zmass); //tirar
         //printf("\n  O inverso da massa total eh: %f. \n", ivmasstot);
                  
         //AMORTECIMENTO
         printf("\n  O amortecimento critico eh: %f,\n  qual serah o valor do amortecimento (gn)? ", 2.0*sqrt(kn/zmass));
         scanf("%f", &gn);
         
         //determinaçao do passe do tempo T=1/f, MH-> f=sqrt(k/m), tempo é discreto
         dt=1.0/(sqrt(kn*zmass))/100; //somente para que o passe de tempo seja bem menor q o periodo de oscilacao
         printf("\n  dt=%f.\n", dt);         
                  
         dt2s2=dt*dt/2;
         c1=dt2s2/dt;
         
         //parametros iniciais e numero de particulas adicionadas
         printf("\n  Qual o numero de particulas que entrarao no sistema? ");
         scanf("%d", &irep);
         for(i=0; i<npap; i++)
         {
                  v[0][i]=0.0; //velocidade eixo x
                  v[1][i]=0.0;            //eixo y
                  a[0][i]=0.0; //aceleraçao
                  a[1][i]=0.0;
                  rot1[i]=0.0; //posição angular, arbitrária
                  rot2[i]=0.0; //velocidade angular
                  rot3[i]=0.0; //aceleraçao angular
         }
         printf("\n  Constante q multiplica o raio da particula (valor entre 0.5 e 2.0)? "); //multiplicará o raio máximo
         scanf("%f", &xray);
         printf("\n  Qual valor de polidispersividade (entre 0 e 1)? "); //para colocar esferas novas com variedades de tamanhos
         scanf("%f", &dhr);
         //printf("\n  Qual valor que multiplicará kn e ks (valor entre 0.1 e oo)? "); //relacionada com a rigidez das esferas adicionais
         //scanf("%f", &cofkn);
	 cofkn = 10;
         printf("\n  "); 
	 SystemPause();
         return;         
}

void putball() //calcular uma posição vazia para inserir nova partícula
{
     float xsum, ysum, xdist, ydist, xi, yi, xj, yj, xmin, xmin0;
     int icont, lista[graosMax], i, j, itr0, itr1, itr;
     
     nball++;
     npap++;
     r[0][npap-1]=0.0+0.00001*(0.5-rand0()); //posicao da proxima particula colocada, sendo ela no centro do hexagono, mas não será ela
     r[1][npap-1]=0.5;
     v[0][npap-1]=0.0; //velocidades e acelerações iniciais são nulas
     v[1][npap-1]=0.0;
     a[0][npap-1]=0.0;
     a[1][npap-1]=0.0;
     xrmin = xray*xrmax - dhr*xray*xrmax;
     xrand = rand0(); 
     xr[npap-1]= xrmin + dhr*xray*xrmax*xrand; //tamanho da esfera adicionada
     printf ("\n xrmin = %f, xr[npap-1] = %f, dhr*xrand*xray*xrmax = %f", xrmin, xr[npap-1], dhr*xrand*xrmax*xray); //tirar dps, somente para conferir
     //como nova particula eh inserida ao sistema, calcular os parametros novamente:
//     zmass=0.0;
//     ivmasstot=0.0; //mudei!!! (AA)
     i=npap-1; //mudei!!! (AA)
     ivmass[i]=(xrmax*xrmax)/(xr[i]*xr[i]);
     ivmominit[i]=2.0*ivmass[i]/(xr[i]*xr[i]);
//   if(ivmass[i]>zmass) zmass=ivmass[i];
     ivmasstot=ivmasstot+1.0/ivmass[i];
     ivmasstot=1.0/ivmasstot;
     xr[npap-1]=xr[npap-1]/5000.0; //raio inicial para crescimento da particula
     
     //esta parte eh responsavel por descobrir quais os graos que estao dentro do orificio
     xsum=0.0; 
     ysum=0.0;
     icont=0;
     for(i=0; i<(npap-1); i++) //calcular distancia entre um grao qualquer e o grao adicionado
     {
              xi=(r[0][i]-r[0][npap-1]);
              yi=(r[1][i]-r[1][npap-1]);
              if ( (xi*xi+yi*yi) < (9.0*xrmax*xrmax) )
              {
                   xsum=xsum+r[0][i]; //somar as distancias das particulas que estao dentro do orificio
                   ysum=ysum+r[1][i];
                   lista[icont]=i; //lista começa na posiçao zero (pq sim), mas as posiçoes ocupadas do vetor = icont /gravar posiçao do grao
                   //printf("\n\n  xr[%d]=%f, r[0][%d]=%f, r[1][%d]=%f", i, xr[i], i, r[0][i], i, r[1][i]); 
                   icont++; //contar quantas particulas estao dentro do orificio
              }
     }
     //geralmente, o centro de massa de n particulas eh um local vazio, portanto:
     if(xsum>0.0) r[0][npap-1]=xsum/(1.0*icont);  //mudei! (AA)
     else r[0][npap-1] = 0.0;
     if(ysum>0.0) r[1][npap-1]=ysum/(1.0*icont); 
     else r[1][npap-1]=0.1;

     //printf("%f %f %f %d\n", r[0][npap-1],r[1][npap-1],xr[npap-1],npap-1);
     //porém se isto não for verdadeiro:             
     for(i=0; i<icont; i++) 
     {
              xi=r[0][lista[i]]-r[0][npap-1];
              yi=r[1][lista[i]]-r[1][npap-1];
              xdist=(xr[lista[i]]*xr[lista[i]]);
              
              xmin=1.0;
              xmin0=1.0;
              itr1=0;
              if( ( (xi*xi) + (yi*yi) ) < xdist ) //se o modulo^2 da distancia do ponto ate raio da particula for menor que o raio^2 
              {
                    itr=i;
                    for(j=0; j<icont; j++)
                    {
                             if(j!=i)
                             {
                                     xj=r[0][lista[j]]-r[0][npap-1];
                                     yj=r[1][lista[j]]-r[1][npap-1];
                                     ydist= xj*xj+yj*yj;
                                     if(ydist<xmin)
                                     {
                                          itr0=itr1;
                                          itr1=j;
                                          xmin0=xmin;
                                          xmin=ydist;
                                     }
                                     else if(ydist<xmin0)
                                     {
                                          itr0=j;
                                          xmin0=ydist;
                                     }
                             }
                    }
                    xsum=r[0][lista[itr]]+r[0][lista[itr0]]+r[0][lista[itr1]];
                    ysum=r[1][lista[itr]]+r[1][lista[itr0]]+r[1][lista[itr1]];
                    r[0][npap-1]=1.0*xsum/3;
                    r[1][npap-1]=1.0*ysum/3;
                    //printf("\n\n  grãos (quantidade) = %d \n\n", icont);
              }
     }

     return;
}

void recherche_voisins1()
{
              float x1, x12, xi, yi, xij, yij, dij;
              int icon, npoint, i, j;
              x1 = 2.5*xrmax; //nao funcionou com 2.2             
              if (xray>1.0) x1=x1*xray;// MUDEI AQUI (AA)
	          x12 = x1*x1;
              ior[ntotal+1] = 0; 
              icon = 1;
              npoint = 0;

              for(i=0; i<npap; i++) //comparar o grão i com os outros grãos maiores que i
              {
                       xi = r[0][i];
                       yi = r[1][i];
                       for(j=i+1; j<npap; j++) 
                       {
                              xij = r[0][j] - xi;
                              yij = r[1][j] - yi;
                              dij = xij*xij + yij*yij;
                              if ( dij < x12 ) //se a distância for menor do que a escolhida, então é vizinho
                              {
                                     npoint++; //número total de vizinhos
                                     liste[0][npoint] = i; //esta matriz começa da posição 1
                                     liste[1][npoint] = j;

                                     if( ( ior[icon] = i ) && ( iex[icon] = j ) )
                                     {
                                              io[npoint] = 0; //verdadeiro
                                              icon++;
                                     }
                                     else io[npoint] = 1; //falso                                     
                              }   
                       }
              }
              nl = npoint;
              return;
}

void predicteur() //prever quais serão as velocidades e acelerações dos grãos tanto linear quanto angular
{
        int i;
        float vi1, vi2, ai1, ai2, rt2, rt3;
        for(i=0; i<npap; i++)
        {
                 vi1 = v[0][i]; 
                 vi2 = v[1][i];
                 ai1 = a[0][i];
                 ai2 = a[1][i];
                 rp[0][i] = r[0][i] + vi1*dt + ai1*dt2s2;
                 rp[1][i] = r[1][i] + vi2*dt + ai2*dt2s2;
                 vp[0][i] = vi1 + ai1*dt;
                 vp[1][i] = vi2 + ai2*dt;
                 ap[0][i] = ai1;
                 ap[1][i] = ai2;
                 rt2 = rot2[i];
                 rt3 = rot3[i];
                 rot1p[i] = rot1[i] + dt*rt2 + dt2s2*rt3; 
                 rot2p[i] = rt2 + rt3*dt;
                 rot3p[i] = rt3;   
        }
        if ( (itaux % 2) == 0 ) xr[npap-1] = xr[npap-1] + (xrmin + dhr*xrand*xray*xrmax)/5000;  /*ir aumentando o tamanho do novo grão adicionado*/
}

void detectcontacts()
{
             int il, i, j;
             float xij, yij, dij, xr2, hij;
             ncont= 0;
             icont0=0;
             for(i=0; i<npap; i++) nnvois[i]=0;
             for(il=1; il<=nl; il++)
             {
                      i = liste[0][il]; //abrir a lista salva 
                      j = liste[1][il];
                      xij = rp[0][j]-rp[0][i]; //já utiliza as posições previstas
                      yij = rp[1][j]-rp[1][i];
                      dij = xij*xij + yij*yij;
                      xr2 = ( xr[i]+ xr[j] )*( xr[i] + xr[j] );
                      if( io[il]==0 ) icont0++;
                      if ( dij < xr2 )
                      {
                              nnvois[i]++; //quantas partículas estão em contato com a partícula i (coluna 0)
                              nnvois[j]++; //em contato com a partícula j coluna 1)
                              ncont++;
                              ior[ncont] = i; //primeira coluna
                              iex[ncont] = j; //segunda coluna
                              dij = sqrt(dij); //distância entre a partícula i e j
                              hij = dij - xr[i] - xr[j]; //interpenetração, se for negativa, os grãos estão em contato
                              eij[ncont] = hij;
                              xnij[0][ncont] = xij/dij; //cosseno do ângulo de contato
                              xnij[1][ncont] = yij/dij; //seno do ãngulo de contato
                              if(io[il]==0) react[ncont] = react0[icont0]; 
                              else react[ncont] = 0.0; 
                              io[il] = 0; //verdadeiro: existe contato, importante para a proxima vez que for detectado o contato, sabermos se ele ja existia
                      }
                      else io[il] = 1; //nao existe contato
             }
             ntotal = ncont;
             return;
}

void calculforces()
{
            int il, i, j;
            float xn1, xn2, xt1, xt2;
            float fn, ft, fx, fy, vijn, vijt, fnel, ftest, fnvi, vp1i, vp1j, vp2i, vp2j;
            for(i=0; i<npap; i++) 
            {
                     fp[0][i] = 0.0;
                     fp[1][i] = 0.0;
                     Gamma[i] = 0.0; 
            }
            igliss=0;//numero de particulas que estão deslizando Ft>Fat
            for(il=1; il<=ncont; il++)
            {
                      i = ior[il];
                      j = iex[il];
                      vp1i = vp[0][i];
                      vp1j = vp[0][j];
                      vp2i = vp[1][i];
                      vp2j = vp[1][j];
                      xn1 = xnij[0][il]; //cosseno   Cálculo das forças normais
                      xn2 = xnij[1][il]; //seno
                      vijn = xn1*(vp1j-vp1i) + xn2*(vp2j-vp2i); //velocidade entre partículas iox e iex em relação à normal
                     
		      int knaux, ksaux;
                      if(i >= npa)
                      {
                           if(j>=npa) knaux = kn*cofkn;
                           else knaux = kn*0.5*(1.0+cofkn);
                      }
                      else
                      {
                          if(j>=npa) knaux = kn*0.5*(1.0+cofkn);
                          else knaux = kn;
                      }
		      fnel = -eij[il]*knaux;
		      ksaux = 3*knaux/4;

                      fnvi = -vijn*gn;  //força de arraste na direção normal

                      fn = fnel + fnvi; //força total na direção normal
                      reacn[il] = fn; //reação normal
                      //forças tangenciais
                      xt1 = -xnij[1][il]; //inverter cosseno pelo seno, pois na tangencial o ângulo é complementar ao ângulo na direção normal
                      xt2 = xnij[0][il];
                      vijt = xt1*(vp1j-vp1i)+xt2*(vp2j-vp2i) - rot2p[i]*xr[i]-rot2p[j]*xr[j]; //velocidade tangencial v angular -> v=w*r
                      ft = react[il];
                      ft = ft - ksaux*vijt*dt; // ft - k*x
                      ftest = frott*fnel; //força de atrito
                      
		      if( (fabs(ft)) > ftest )
		      //if ( (sqrt(ft*ft)) > ftest ) 
                      {
                         if (( (nnvois[i]) =! 1 ) && ( (nnvois[j]) =! 1 )) igliss++; 
                         if (ft>0) ft = ftest;
                         else ft = -ftest;
                      }
                      react[il] = ft; 
                      //resultantes das forças
                      fx = fn*xn1 + ft*xt1;
                      fy = fn*xn2 + ft*xt2;
            
                      fp[0][i] = fp[0][i] - fx;
                      fp[1][i] = fp[1][i] - fy;
                      fp[0][j] = fp[0][j] + fx;
                      fp[1][j] = fp[1][j] + fy;
                      Gamma[i] = Gamma[i] - ft*xr[i]; //torque
                      Gamma[j] = Gamma[j] - ft*xr[j];    
            }
            return;                    
}

void archivagereaction() //arquivar as reações tangenciais
{
     int il;
     for(il=1; il<=ntotal; il++) react0[il] = react[il]; 
     return;     
}

/*int signe(float val1, float val2)
{
	int boolaux;	
	if(val1>0.0)
	{
	     if(val2>0.0) boolaux = 1;
	     else boolaux = 0;
	}
	else
	{
	     if(val2>0.0) boolaux = 0;
	     else boolaux = 1;
	}
	return boolaux;
}

void CundallDamping()
{
	float alpha = 0.70, f1, f2, v1, v2, vr, rm;
	int i;
	for(i=0; i<npap; i++)
	{
	      f1 = fp[0][i];
	      f2 = fp[1][i];
	      v1 = vp[0][i];
	      v2 = vp[1][i];
	      if( (signe(f1,v1)) ) fp[0][i] = f1*(1.0 - alpha);
	      else fp[1][i] = f1*(1.0 + alpha);
	      if( (signe(f2,v2)) ) fp[1][i] = f2*(1.0 - alpha);
	      else fp[1][i] = f2*(1.0 + alpha);

	      vr = rot2[i];
	      rm = Gamma[i];
	      if( (signe(vr,rm)) ) Gamma[i] = rm*(1.0 - alpha);
	      else Gamma[i] = rm*(1.0 + alpha);
	}
	return;
}*/

void correcteur()
{
     int i;    
     for(i=0; i<npap; i++)
     {
              a[0][i] = fp[0][i]*ivmass[i];
              a[1][i] = fp[1][i]*ivmass[i];
              //v[0][i] = vp[0][i] + c1*(a[0][i] - ap[0][i]);
              //v[1][i] = vp[1][i] + c1*(a[1][i] - ap[1][i]);
              v[0][i] = (1.0-frot2)*(vp[0][i] + c1*(a[0][i] - ap[0][i])); //drag friction 
              v[1][i] = (1.0-frot2)*(vp[1][i] + c1*(a[1][i] - ap[1][i]));
              r[0][i] = rp[0][i];
              r[1][i] = rp[1][i];
              rot3[i] = Gamma[i]*ivmominit[i];
              rot2[i] = rot2p[i] + c1*(rot3[i]-rot3p[i]);
              rot1[i] = rot1p[i]; 
     }
     return;
}

void affichage()
{
     //call profon fazer dps
     int i, nsi, nsi1;
     float ymax, cineti, vqrt, ff;
     cineti = 0.0;
     ymax = 0.0;
     
     for(i=0; i<npap; i++)
     {
              vqrt = v[0][i]*v[0][i] + v[1][i]*v[1][i];
              cineti = cineti + vqrt;  
     }
     nsi = 0;
     nsi1 = 0;
     for(i=0; i<npap; i++)
     {
              if(nnvois[i]>0) nsi++;
              if(nnvois[i]<1) nsi1++;
     }
     ff = 0.0;
     for(i=npa; i<npap; i++) ff=ff-fp[1][i];
     printf("\n  ntotal=%d, nsi=%d, nsi1=%d, cineti=%le", ntotal, nsi, nsi1, cineti); 
     return;  
}

void sauveconf(int num) 
{
                int i, j, il;
				
		char fname[25];
		sprintf(fname, "%s_%04d.txt", datnameaux2, num); //sprintf(fname, "DMconf%03s%02d_%04d.txt", nom, nq, num);
		printf("\n\n  Nome da configuracao a ser salva: %s \n", fname);
                f2=fopen(fname, "w");
                fprintf(f2, "%d %d\n", npap, npap); printf(" \n  npap=%d", npap);
                for(i=0; i<npap; i++) fprintf(f2, "%f %f %f %f %f\n",r[0][i], r[1][i], xr[i], ivmass[i], ivmominit[i]);
                fprintf(f2, "%f %f %f %f %f %f\n", dt, kn, gn, frott, ks, ivmasstot); 
                fprintf(f2, "%d %d\n", ncont, ntotal);             
                for(il=1; il<=ntotal; il++)
                {
                       i = ior[il];
                       j = iex[il];
                       fprintf(f2, "%d %d %d %f %f %f %f\n", il, i+1, j+1, reacn[il], react[il], xnij[0][il], xnij[1][il]);
                } 
                fclose(f2);
                return;  
}

