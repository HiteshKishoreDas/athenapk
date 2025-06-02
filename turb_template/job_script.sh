#!/bin/sh
#SBATCH -o ./out.%j
#SBATCH -e ./err.%j
#SBATCH -J turb_test
#SBATCH -p p.gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mail-type=none
#SBATCH --mail-user=hitesh@mpa-garching.mpg.de
#SBATCH --time=00:30:00
#SBATCH -D ./

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
srun /ptmp/mpa/hitesh/athenapk/build-gpu/bin/athenaPK -i turb_with_tracers.in>turb.out

echo "Elapsed: $(($SECONDS / 3600))hrs $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
echo "Boom!"