
#module use -a /scratch2/NCEPDEV/marineda/Jong.Kim/save/modulefiles
#module load anaconda/3.15.1

exp='exp3'
OBSTYPE='surface'
taskdir=/scratch1/BMC/zrtrr/llin/210511_jedi/61_mhu_test/test_v01/case2/output

VarName='air_temperature'
filename="ufo_sfc_2021010612_t_0000.nc4"
python list_ufo_omb.py $taskdir/$filename $OBSTYPE $VarName $exp

VarName='specific_humidity'
filename="ufo_sfc_2021010612_q_0000.nc4"
python list_ufo_omb.py $taskdir/$filename $OBSTYPE $VarName $exp

VarName='eastward_wind'
filename="ufo_sfc_2021010612_uv_0000.nc4"
python list_ufo_omb.py $taskdir/$filename $OBSTYPE $VarName $exp

VarName='northward_wind'
filename="ufo_sfc_2021010612_uv_0000.nc4"
python list_ufo_omb.py $taskdir/$filename $OBSTYPE $VarName $exp
