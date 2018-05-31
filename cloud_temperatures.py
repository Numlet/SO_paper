from  base_imports import *

list_params=['SATELLITE','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']


clouds=['C3']
clouds=['C1','C2','C3']
c_clouds=['b','r','g']
plt.close()
plt.close()
icol=0
for cloud in clouds:
#    plt.figure()
    for iparam in list_params[1:]:
        iparam='VT17_MEAN'
        iparam='M92'
        data=np.load(pspc_fol+'temps_'+cloud+'_'+iparam+'.npy')
    #    data=data[data>-35]
        plt.hist(data[~np.isnan(data)],30,normed=True,alpha=0.65,label=cloud,color=c_clouds[icol])
        plt.axvline(np.nanmean(data),color=c_clouds[icol])
        icol=icol+1
#        plt.yscale('log')
    plt.legend(loc='best')
    plt.savefig(sav_fol+cloud+'_temperatures.png')
list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
icol=0
#for param in list_params[2:]:
#%%
#temps=data.flatten()
#temps_clean=temps[~np.isnan(temps[:])]
#temps_clean_sorted=np.sort(temps_clean)
#INP=param[iparam](data)
#INP[INP==0]=np.nan
#INP=INP.flatten()
#INP=INP[np.logical_not(np.isnan(INP))]
#
#INP_clean=INP[~np.isnan(INP[:])]
#INP_clean_sorted=np.sort(INP_clean)
#plt.hist(INP_clean_sorted,np.logspace(-4,6,100),alpha=0.6,label='now calculated')
#plt.hist(INP,np.logspace(-4,6,100),alpha=0.6,label='now calculated')
#%%

list_params=['M92','VT17_MEAN']
for iparam in list_params:
    plt.figure()
#    iparam='M92'
    INP=param[iparam](data)
#    plt.close()
    icol=0
#    param='M92'
#    plt.hist(INP[~np.isnan(INP)],np.logspace(-4,6,100),alpha=0.6,label='now calculated')
    for cloud in clouds:

        data=np.load(pspc_fol+'INP_'+cloud+'_'+iparam+'.npy')
        plt.title(iparam)
        plt.hist(data[~np.isnan(data)],np.logspace(-4,6,100),alpha=0.6,label=cloud,color=c_clouds[icol],normed=1)
        plt.axvline(np.nanmedian(data),c=c_clouds[icol])
	icol=icol+1
        plt.xscale('log')
#        plt.yscale('log')
        plt.legend()
    plt.savefig(sav_fol+iparam+'_INP.png')


##%%
#np.save('test.npy',INP)
#INP2=np.load('test.npy')
#
#plt.hist(INP2[~np.isnan(INP2)],np.logspace(-4,6,100),alpha=0.6,label='now calculated')
##plt.yscale('log')
#plt.xscale('log')
##plt.hist(INP[~np.isnan(INP)],np.logspace(-4,6,100),alpha=0.6,label='now calculated')

