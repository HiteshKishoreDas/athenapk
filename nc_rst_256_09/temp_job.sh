#!/bin/sh
#SBATCH -o ./!!JOBNAME!!.out.%j
#SBATCH -e ./!!JOBNAME!!.err.%j
#SBATCH -J !!JOBNAME!!
#SBATCH -p !!PARTITION!!
#SBATCH --gres=gpu:!!GPU_TYPE!!:!!NUM_GPUS!!
#SBATCH --nodes=!!NODES!!
#SBATCH --ntasks-per-node=!!NTASKS!!
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ankitad@mpa-garching.mpg.de
#SBATCH --time=!!WALLTIME!!
#SBATCH -D !!WORKDIR!!

set -e
SECONDS=0

module purge
module load cuda/11.6
module load clang/18
module load intel/21.7.1
module load openmpi/4
module load hdf5-mpi/1.14.1
module load gcc/11
module list

# Run the program:
srun !!EXECUTABLE!! -i !!INPUTFILE!! problem/turbulence/rescale_once_on_restart=true -r /ptmp/mpa/ankitad/athenapk/nc_256_09/parthenon.restart.final.rhdf > !!JOBNAME!!.out
echo "Elapsed: $(($SECONDS / 3600))hrs $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
