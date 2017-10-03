#include <stdio.h>
#include <math.h>

//#include <windows.h>

#include <time.h>
#define iA 843314861
#define iB 453816693
#define iM 1073741824

FILE *f1;
FILE *f2;
/*****************declaração  funções*****************************/
float rand0();
void sauveconf();
int anint(float x);
void recherche_Voisins1();
void inicio();
void preditor();
void detectcontacts();
void calculoforcas();
void corretor();
void verifequilibre();
void profon();
void affichage();
void sauvconf();
int archivagereaction();
/****************variáveis globais********************************/

const int tamanho1 = 110000;
const int tamanho2 = 440000;
const int tamanho3 = 3000000;

char nom[3],nvieux[3],nnq[2];
int it,isem = 98765431;
int nq,npa,npap,ncont,ntotal,nl,nlt,ifreqv,iaff,isauve,mlh,ncell,icont0,igliss;
clock_t t_inicial;
static double rot2[tamanho1],rot3[tamanho1],rot1[tamanho1];
float kn,ks,dt2s2,frott,c1,xrmax,tolff,ivmasstot,gn,erreurtotal,viol,equil;
double dt;
static double xr[tamanho1],r[2][tamanho1],rp[2][tamanho1], vp[2][tamanho1];
static int   ior[tamanho2],iex[tamanho2],liste[2][tamanho3],io[tamanho3];
static double rot1p[tamanho1],rot2p[tamanho1],rot3p[tamanho1];
static double gama[tamanho1];
static double ap[2][tamanho1],xrp[tamanho1],nnvois[tamanho1],eij[tamanho2],xnij[2][tamanho2];
static double fp[2][tamanho1],fpp[2][tamanho1];
static double ivmass[tamanho1],ivmominit[tamanho1],reacn[tamanho2], react0[tamanho2],react[tamanho2],a[2][tamanho1];
static double v[2][tamanho1];


int main ()
{
    t_inicial = clock();
    inicio();
    recherche_Voisins1();
    it=0;
    equil=1;
    while((equil!=0) && it < (1000000))
    {
        it++;
        if((it%ifreqv)==0) recherche_Voisins1();
        preditor();
        detectcontacts();
        calculoforcas();
        archivagereaction();
        corretor();

        if((it%iaff)==0)
        {
            verifequilibre();
            affichage();
        }
        if ((it%isauve)==0)  sauvconf();
    }

    printf("'EQUILIBRE !'\n");

    affichage();
    sauvconf();

//    Sleep(8000);
}



void inicio()
{
    int iq1,iq2,i,j,irep,lecforces,ill,il;
    float xmax,zmass;
    char datname[16];

    printf(" Digite nq \n");
    //scanf("\n %d",&nq);
    nq = 100;

    printf(" Digite o nome da configuração de inicio (o nome deve conter 3 letras: ex: af0\n)");
    scanf( "\n %s",&nvieux);
    //nvieux = 'paa';

    printf(" digite kn \n");
    //scanf("\n %f",&kn);
    kn = 1000;

    printf(" Digite ks\n");
    //scanf("\n %f",&ks);
    ks = 750;

    printf("Digite o coeficiente de atrito \n");
    scanf("%f",&frott);
    //frott = 0.5;

    printf(" Digite a frequencia de exibiçao\n");
    //scanf("\n%d",&iaff);
    iaff = 1000;

    printf("Digite a frequencia calculada vizinhos\n");
    //scanf("\n%d",&ifreqv);
    ifreqv = 100;

    printf(" Digite a frequencia a ser guardada et verif EQUILIBRE\n");
    //scanf("\n%d",&isauve);
    isauve = 1000;

    printf(" Havera leitura das forças iniciais? (0=sim)(1=nao)\n");
    //scanf("\n %d",&lecforces);
    lecforces = 1;

    printf("Digite o erro sobre o peso\n");
    //scanf("\n %f",&tolff);
    tolff = 0.0000001;

    printf("\nOk...\n");

    iq1 = nq / 10;
    iq2 = nq - 10 * iq1;

    //nnq[0] = char(iq1 + 48);
    //nnq[1] = char(iq2 + 48);
    nnq[0] = 'C';
    nnq[1] = 'M';

    ncont = 0;
    ntotal = 0;

    /***************-----leitura dados iniciais**************/
    datname[0] = 'D';
    datname[1] = 'M';
    datname[2] = 'c';
    datname[3] = 'o';
    datname[4] = 'n';
    datname[5] = 'f';
    datname[6] = nvieux[0];
    datname[7] = nvieux[1];
    datname[8] = nvieux[2];
    datname[9] = nnq[0];
    datname[10] = nnq[1];
    datname[11] = '.';
    datname[12] = 'd';
    datname[13] = 'a';
    datname[14] = 't';
    datname[15] = '\0';

    printf("datname: %s\n", datname);

    printf(" Digite o nome da configuração a ser guardada (o nome deve conter 3 letras: ex: af1\n)");
    scanf( "\n %s",&nom);
    //nom = "FFF";


    f1=fopen(datname,"r");
    fscanf(f1,"%d %d \n",&npa,&npap);
    for(i=1; i<=npap; i++)
    {
        fscanf(f1,"%le %le %le",&r[0][i],&r[1][i],&xr[i]);

    }
    if (lecforces==0)
    {
        fscanf(f1,"%le %le %le %le %le %le \n",&dt,&kn,&gn,&frott,&ks,&ivmasstot);

        fscanf(f1,"%d %d",&ncont,&ntotal);
        printf("ncont, ntotal = %d %d",ncont, ntotal);
        for (ill=1; ill<=ntotal; ill++)
        {
            fscanf(f1,"%d %d %d %le %le ",&il,&ior[il],&iex[il],&reacn[il],&react0[il]);
        }
    }
    fclose(f1);

    /*********-----Numero de celulas para a pesquisa dos vizinhos**********/
    mlh = (int)(sqrt(float(npa)/10.0));
    if (mlh<=3)
    {
        printf("\n Atenção não basta celula mlh = %d \n",mlh);
        mlh=3;
    }
    ncell = mlh*mlh;
    printf("Numero de celulas para pesquisa dos vizinhos = %d\n ",ncell);

    /*********----Massa de particulas na amostra, invertido
    -----A maior particula tem massa de 1 adim*************/
    zmass = 0.0;
    ivmasstot = 0.0;
    xrmax = -1E20;
    for(i =1; i<=npap; i++)
    {
        xrmax = (xr[i]>xrmax)?xr[i]:xrmax;
    }
    for (i=1; i<=npa; i++)
    {
        ivmass[i] = xrmax*xrmax / (xr[i]*xr[i]);
        ivmominit[i] = 2E0 * ivmass[i] /(xr[i]*xr[i]);
        zmass = (ivmass[i]>zmass)?ivmass[i]:zmass;
        ivmasstot = ivmasstot + (1/ivmass[i]);
    }
    ivmasstot = 1.0/ivmasstot; /*inverse de la masse totale;*/
    /************-----Amortecimento***************/
    printf(" gn ? < %f \n ",2.0*sqrt(kn/zmass));
    scanf("%f",&gn);
    /************-----Determinaçao du pas de tempo*************/
    dt = 1/sqrt(kn*zmass)/50; /* ! xx/50 -> arbitraire!*/
    printf("dt = %f \n",dt);
    /**********-----Coeficiente de preditor-corretor**************/
    dt2s2 = dt*dt/2;
    c1 = dt2s2/dt;
    /***********-----Inicialização multipla**************/
    printf("Iniciar com velocidades aleatorias? (0=sim)(1=nao)\n");
    //scanf("%d",&irep);
    irep = 1;

    printf("\nOk...\n");


    if (irep==0)
    {
        isem = 987654321;
        for (i=1; i<=npap; i++)
        {
            v[0][i] = pow(0.05*(-1),i) * rand0();
            v[1][i] = pow(0.05*(-1),(i+1))* rand0();
        }
    }
    else
    {
        for(i=1; i<=npap; i++)
        {
            v[0][i] = 0.0;
            v[1][i] = 0.0;
        }

    }
    for( i=1; i<=npap; i++)
    {
        a[0][i] = 0.0;
        a[1][i] = 0.0;
        rot2[i] = 0.0;
        rot3[i] = 0.0;
    }
}
void recherche_Voisins1()
{
    /**************** Pesquisa vizinhos 1 *************/
    /***********Pesquisa abrupta vizinhos! (en N**2)
    Uso de \ amostras muito pequenas (npa < 50)**************/
    int icon, npoint,i,j;
    double x1,x12,xi,yi, xij,yij,dij;


    x1 =  2.2*xrmax;
    x12 = x1*x1;
    ior[ntotal+1] = 0;
    icon = 1;
    npoint = 0;

    /***********vizinhança entre grãos livres ***********/
    for (i=1; i<=npa; i++)
    {
        xi = r[0][i];
        yi = r[1][i];

        for (j=i+1; j<=npa; j++)
        {
            xij = r[0][j] - xi;
            yij = r[1][j] - yi;
            xij = xij - anint(xij);
            dij = (xij*xij + yij*yij);
            if (dij < x12)
            {
                npoint = npoint + 1;
                liste[0][npoint] = i;
                liste[1][npoint] = j;

                if ((ior[icon]==i)&&(iex[icon]==j))
                {
                    io[npoint] = 1;
                    icon = icon + 1;
                }
                else
                {
                    io[npoint] = 0;
                }
            }
        }
    }
    nl = npoint;
    /***********vizinhança entre grãos e grãos livres fixos*************/

    for (i=1; i<=npa; i++)
    {
        xi = r[0][i];
        yi = r[1][i];


        for (j =npa+1; j<=npap; j++)
        {
            xij = r[0][j] - xi;
            yij = r[1][j] - yi;
            xij = xij - anint(xij);
            dij = (xij*xij + yij*yij);

            if (dij < x12)
            {
                npoint = npoint + 1;
                liste[0][npoint] = i;
                liste[1][npoint] = j;
                if((ior[icon]==i)&&(iex[icon]==j))
                {
                    io[npoint] = 1;
                    icon = icon + 1;
                }
                else
                {
                    io[npoint] = 0;
                }
            }
        }
    }
    nlt = npoint;

    return;

}
void preditor()

{
    int i;
    double vi1, vi2,ai1, ai2,rt2,rt3;
    /************Predictions sur les particules libres***********/

    for  (i =1; i<=npa; i++)
    {
        vi1 = v[0][i];
        vi2 = v[1][i];
        ai1 = a[0][i];
        ai2 = a[1][i];
        r[0][i] = r[0][i] - anint(r[0][i]);
        rp[0][i] = r[0][i] + dt*vi1 + dt2s2*ai1;
        rp[1][i] = r[1][i] + dt*vi2 + dt2s2*ai2;
        vp[0][i] = vi1 + dt*ai1 ;
        vp[1][i] = vi2 + dt*ai2 ;
        ap[0][i] = ai1 ;
        ap[1][i] = ai2 ;
        rt2 = rot2[i];
        rt3 = rot3[i];
        rot1p[i] = rot1[i] + dt*rt2 + dt2s2*rt3 ;
        rot2p[i] = rt2 + dt*rt3 ;
        rot3p[i] = rt3;
    }

    return;
}
/**********************definição função rand0()***********************/
float rand0()
{
    float aux,x,rand0;

    aux = 0.5/float (iM);

    isem = isem*iA + iB;
    {
        if(isem < 0)
        {
            isem = (isem + iM )+iM;
        }
    }
    x = isem*aux;
    rand0=x;

    printf("% f %f \n",x,aux);
    return x;
}
/***************************definiçao função anint ************************************************/
int anint(float x)
{
    int ix;

    if(x>=0)    x=x+0.5;
    else        x=x-0.5;

    ix = (int)x;

    return (ix);
}
/******************detecta contatos************************/
void detectcontacts()

{
    int i,j,il;
    double x1,x12,xi,yi,xij,yij,dij,xr2,hij;

    /***********Inicializaçoes*******************/
    ncont = 0;
    icont0 = 0;
    for(i = 1; i<=npa; i++)
    {
        nnvois[i] = 0;
    }

    /**************Contato entre grãos livres******************/
    for(il=1; il<=nl; il++)
    {
        i=liste[0][il];
        j=liste[1][il];
        xij = rp[0][j] - rp[0][i];
        yij = rp[1][j] - rp[1][i];
        xij = xij - anint(xij); /***! CL periodique***/
        dij = xij*xij + yij*yij;
        xr2 = (xr[i]+xr[j])*(xr[i]+xr[j]);
        if(io[il]) icont0 = icont0 + 1;/***!compteur pour recuperation react**/

        if (dij<xr2)
        {
            nnvois[i] = nnvois[i] + 1;
            nnvois[j] = nnvois[j] + 1;
            ncont = ncont + 1;
            ior[ncont] = i;
            iex[ncont] = j;
            dij = sqrt(dij);
            hij = dij - xr[i] - xr[j];
            eij[ncont] = hij;
            xnij[0][ncont] = xij / dij;
            xnij[1][ncont] = yij / dij;

            /***recuperation des forces tangentielles***/
            if (io[il])
            {
                react[ncont] = react0[icont0];
            }
            else
            {
                react[ncont] = 0;
            }

            io[il] =1;
        }
        else
        {
            io[il] = 0;
        }
    }
    ntotal = ncont;
    /***Contact entre grains libres et paroi***/
    for(il =nl+1; il<=nlt; il++)
    {
        i=liste[0][il];
        j=liste[1][il];
        xij = r[0][j] - rp[0][i];
        xij = xij - anint(xij);/** CL periodique**/
        yij = r[1][j] - rp[1][i];
        dij = xij*xij + yij*yij;
        xr2 = (xr[i]+xr[j])*(xr[i]+xr[j]);
        if (io[il]) icont0 = icont0 + 1; /***!compteur pour recuperation react***/
        {
            if (dij<xr2)
            {
                nnvois[i] = nnvois[i] + 1;
                ntotal = ntotal + 1;
                ior[ntotal]= i;
                iex[ntotal] = j;
                dij = sqrt(dij);
                hij = dij - xr[i] - xr[j];
                eij[ntotal] = hij ;
                xnij[0][ntotal] = xij / dij;
                xnij[1][ntotal] = yij / dij;


                /************recuperation des forces tangentielles***********/
                if (io[il])
                {
                    react[ntotal] = react0[icont0];
                }
                else
                {
                    react[ntotal] = 0;
                }
                io[il] = 1;
            }
            else
            {
                io[il] = 0;
            }
        }
    }

    return;
}
/******************* Calculo das Forças******************/

void calculoforcas()
{
    int i,j,il;
    double xn1,xn2,xt1,xt2;
    double fn,ft,fx,fy,vijn,vijt,ftest,vp1i,vp1j,vp2i,vp2j,fnel,fnvi ;

    /***********Inicializações*********/

    for ( i =1; i<=npa; i++)
    {
        fp[0][i] = 0;
        fp[1][i] = - ivmasstot / ivmass[i]; // Gravit\'e//
        gama[i] = 0;
    }
    for ( i = npa+1; i<=npap; i++)
    {
        fpp[0][i] = 0;
        fpp[1][i] = 0;
    }
    igliss = 0;

    /**************Contatos entre grãos livres**************/
    for (il = 1; il<= ncont; il++)
    {
        i = ior[il];
        j = iex[il];
        vp1i = vp[0][i];
        vp1j = vp[0][j];
        vp2i = vp[1][i];
        vp2j = vp[1][j];
        /********Forças normais***********/
        xn1 = xnij[0][il];
        xn2 = xnij[1][il];
        vijn = xn1*(vp1j-vp1i)+xn2*(vp2j-vp2i);
        fnel = - eij[il]*kn;
        fnvi = - vijn*gn;
        fn = fnel + fnvi;
        reacn[il] = fn;
        /*************Forças tangenciais****************/
        xt1 = -xnij[1][il];
        xt2 =  xnij[0][il];
        vijt = xt1*(vp1j-vp1i)+xt2*(vp2j-vp2i) -  rot2p[i]*xr[i] - rot2p[j]*xr[j];
        ft = react[il];
        ft = ft - ks*vijt*dt;
        ftest = frott*fnel;
        if (fabs(ft)>ftest)
        {
            igliss=igliss+1;
            if (ft>0)
            {
                ft =  ftest;
            }
            else
            {
                ft = -ftest;
            }
        }

        react[il] = ft;
        /*******Resultantes das forças**********/
        fx = fn*xn1 + ft*xt1;
        fy = fn*xn2 + ft*xt2;
        fp[0][i] = fp[0][i] - fx;
        fp[1][i] = fp[1][i] - fy;
        fp[0][j] = fp[0][j] + fx;
        fp[1][j] = fp[1][j] + fy;
        gama[i] = gama[i] - ft*xr[i];
        gama[j] = gama[j] - ft*xr[j];
    }

    /**************Contatos grãos livres - graos fixos (paroi)************/
    for( il=ncont+1; il<=ntotal; il++)
    {
        i = ior[il];
        j = iex[il];
        vp1i = vp[0][i];
        vp2i = vp[1][i];
        /*********Forças normais**********/
        xn1 = xnij[0][il];
        xn2 = xnij[1][il];
        vijn = xn1*(-vp1i)+xn2*(-vp2i);
        fnel = - eij[il]*kn;
        fnvi = - vijn*gn;
        fn = fnel + fnvi;
        reacn[il] = fn;
        /*************Forças tangenciais************/
        xt1 = -xnij[1][il];
        xt2 =  xnij[0][il];
        vijt = xt1*(-vp1i)+xt2*(-vp2i) - rot2p[i]*xr[i];
        ft = react[il];
        ft = ft - ks*vijt*dt;
        ftest = frott*fnel;

        if(fabs(ft)>ftest)
        {
            igliss=igliss+1;
            if (ft>0)
            {
                ft =  ftest;
            }
            else
            {
                ft = -ftest;
            }
        }

        react[il] = ft;
        /***************Bilan des forces***************/
        fx = fn*xn1 + ft*xt1;
        fy = fn*xn2 + ft*xt2;
        fp[0][i] = fp[0][i] - fx;
        fp[1][i] = fp[1][i] - fy;
        fpp[0][j] = fpp[0][j] + fx;
        fpp[1][j] = fpp[1][j] + fy;
        gama[i] = gama[i] - ft*xr[i];

    }

    return;
}


/**********************Correcteur*****************/
void corretor()
{
    int i;
    /*******************Correction sur les particules libres****************/
    for (i = 1; i<=npa; i++)
    {
        a[0][i] = fp[0][i]*ivmass[i];
        a[1][i] = fp[1][i]*ivmass[i];
        v[0][i] = vp[0][i] + c1*(a[0][i]-ap[0][i]);
        v[1][i] = vp[1][i] + c1*(a[1][i]-ap[1][i]);
        r[0][i] = rp[0][i];
        r[1][i] = rp[1][i];
        rot3[i] = gama[i]*ivmominit[i];
        rot2[i] = rot2p[i] + c1*(rot3[i]-rot3p[i]);
        rot1[i] = rot1p[i];
    }

    return;
}


/***************************verificando equilibrio *********************/
void verifequilibre()
{
    int i,il,j;
    double  tolForce, fnel,fx,fy, res1,resrel,ff,aux;
    static double Rmax[tamanho1],fve[2][40000];


    erreurtotal = 0;
    tolForce = 1E-6;

    /*******************Calcul des forces Elastiques (sans amortissement)**************/
    for (i = 1; i<=npa; i++)
    {
        Rmax[i] = 0.0;
        fve[0][i] = 0.0;
        fve[1][i]  = - ivmasstot / ivmass[i];// ! Gravit\'e//
    }
    for (il = 1; il<=ncont; il++)
    {
        i = ior[il];
        j = iex[il];
        fnel = - eij[il]*kn;
        Rmax[i] = (fnel>Rmax[i])?fnel:Rmax[i];
        Rmax[j] =(fnel>Rmax[j])?fnel:Rmax[j];
        fx = fnel*xnij[0][il] - react[il]*xnij[1][il];
        fy = fnel*xnij[1][il] + react[il]*xnij[0][il];
        fve[0][i] = fve[0][i] - fx;
        fve[1][i] = fve[1][i] - fy;
        fve[0][j] = fve[0][j] + fx;
        fve[1][j] = fve[1][j]+ fy;
    }
    for( il = ncont+1; il<=ntotal; il++)
    {
        i = ior[il];
        fnel = - eij[il]*kn;
        Rmax[i] = (fnel>Rmax[i])?fnel:Rmax[i];
        fx = fnel*xnij[0][il] - react[il]*xnij[1][il];
        fy = fnel*xnij[1][il] + react[il]*xnij[0][il];
        fve[0][i] = fve[0][i] - fx;
        fve[1][i] = fve[1][i] - fy;
    }

    res1 = 0;
    resrel = 0;
    for( i = 1; i<=npa; i++)
    {
        if(nnvois[i]>1)
        {
            ff = sqrt(fve[0][i]*fve[0][i] + fve[1][i]*fve[1][i]);
            res1 = (fabs(gama[i])>res1)?fabs(gama[i]):res1;
            res1=(ff>res1)?ff:res1;

            if(Rmax[i]>0)
            {
                aux = 1.0*ff/Rmax[i];
                resrel = (aux>resrel)?aux:resrel;
            }
        }
    }

    erreurtotal = (res1>erreurtotal)?res1:erreurtotal;
    erreurtotal = (resrel>erreurtotal)?resrel:erreurtotal;

    return;

}
void profon()
{

    int i,il;

    /******************Calcul de l'interp\'en\'etration maximale*****************/
    viol = 0.0;
    for( il = 1; il<= ntotal; il++)
    {
        viol = (eij[il]<viol)?eij[il]:viol;
    }
    viol = -viol/(2*xrmax);

    return;
}

/**********************affichage*******************************/

void affichage()
{

    double cineti,ymax,vqrt,ff;
    int i,nsi,nsi1;

    /******************Test des violations ( = profondeurs de penetration)****************/
    profon();
    /***********Energie cinetique totale***********/
    cineti = 0.0;
    ymax = 0.0;
    for( i = 1; i<=npa; i++)
    {
        ymax = (r[1][i]>ymax)?r[1][i]:ymax;
        vqrt = v[0][i]*v[0][i] + v[1][i]*v[1][i];
        cineti = cineti + vqrt;
    }

    nsi = 0;
    nsi1 = 0;
    for( i=1; i<=npa; i++)
    {
        if (nnvois[i]>0) nsi = nsi + 1;
        if (nnvois[i]<=1) nsi1 = nsi1 + 1;
    }

    ff = 0.0;
    for( i = npa+1; i<=npap; i++)
    {
        ff = ff - fpp[1][i];
    }
    f2=fopen ("saida.dat","a");
    fprintf(f2,"%d %d %d %d %le %le %le %le %le %d %le \n", it,ntotal,nsi,nsi1,viol,cineti,ff,erreurtotal,ymax,igliss, float(clock()-t_inicial)/CLOCKS_PER_SEC);
    fclose(f2);
    printf("%d %d %d %d %le %le %le %le %le %d %le \n", it,ntotal,nsi,nsi1,viol,cineti,ff,erreurtotal,ymax,igliss, float(clock()-t_inicial)/CLOCKS_PER_SEC);

    /*********Equilibre atteind ?**************/
    equil = 1;
    if (igliss<1)
    {
        if (nsi1==0)
        {
            if (cineti<1E-7)
            {
                if (fabs(ff-1.0)<=tolff)
                {
                    equil = 0;
                }
            }
        }
    }

    return;
}



/**************Subroutine ArchivageReaction********************/


/**********Archivage des r\'eactions tangentielles*************/
int archivagereaction()
{
    int il;


    for ( il = 1; il<=ntotal; il++)
    {
        react0[il] = react[il];
    }


}
/*************SauveConf************************/
void sauvconf()
{
    //printf("passei no sauveconf\n");
    float xmax, aux;
    int iq1,iq2,i,il,j;
    char datname[16];

    xmax = 0.0;
    for (i = 1; i<=npa; i++)
    {
        aux = sqrt(r[0][i]*r[0][i]);
        xmax = (xmax>aux)?xmax:aux;
    }
    xmax = xmax + 0.5;
    xmax = xmax * 2.0;

    datname[0] = 'D';
    datname[1] = 'M';
    datname[2] = 'c';
    datname[3] = 'o';
    datname[4] = 'n';
    datname[5] = 'f';
    datname[6] = nom[0];
    datname[7] = nom[1];
    datname[8] = nom[2];
    datname[9] = nnq[0];
    datname[10] = nnq[1];
    datname[11] = '.';
    datname[12] = 'd';
    datname[13] = 'a';
    datname[14] = 't';
    datname[15] = '\0';

    //printf("Arquivo %s\n",datname);

    f1=fopen(datname,"w");
    fprintf(f1,"%d %d \n", npa,npap);
    for ( i = 1; i<=npap; i++)
    {
        fprintf(f1,"%f %f %f %f %f \n", r[0][i], r[1][i], xr[i],ivmass[i],ivmominit[i]);
    }
    fprintf(f1,"%f %f %f %f %f %f \n",dt,kn,gn,frott,ks,ivmasstot);
    fprintf(f1,"%d %d \n",ncont,ntotal);
    for(il=1; il<=ntotal; il++)
    {
        i=ior[il];
        j=iex[il];
        fprintf(f1,"%d %d %d %f %le %f %f \n",il,i,j,reacn[il],react[il],xnij[0][il],xnij[1][il]);
    }
    fclose(f1);

    return;
}

