#!/bin/sh
#SBATCH -o ./nc256.out.%j
#SBATCH -e ./nc256.err.%j
#SBATCH -J nc256
#SBATCH -p p.gpu
#SBATCH --gres=gpu:v100:2
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ankitad@mpa-garching.mpg.de
#SBATCH --time=24:00:00
#SBATCH -D /ptmp/mpa/ankitad/athenapk/sim256

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
srun /ptmp/mpa/ankitad/athenapk/build-gpu/bin/athenaPK -i /ptmp/mpa/ankitad/athenapk/sim256/athinput.turb > nc256.out
echo "Elapsed: $(($SECONDS / 3600))hrs $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
