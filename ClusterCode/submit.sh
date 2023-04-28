#!/bin/sh
#SBATCH --job-name=sentiment_analysis
#SBATCH -o OUT.out
#SBATCH -e Err.err
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 1-00:00
#SBATCH -p shared
#SBATCH --mem-per-cpu=8000
##SBATCH --mail-type=ALL
##SBATCH --mail-user=kehang_zhu@fas.harvard.edu
#SBATCH --no-requeue

module load Anaconda3/2020.11
module load cmake/3.17.3-fasrc01;
module load gcc/9.3.0-fasrc01
source activate sentiment

date
# paths

python panic1.py
# nequip-evaluate --model /n/holyscratch01/kozinsky_lab/Kehang/Recrystalization/high-speed5/Li-deployed.pth --dataset-config new-data.yaml --metrics-config metric.yaml

# srun -n $SLURM_NTASKS /n/home09/zkh/lammps/build/lmp -var SEED $RANDOM  -in md_li3_input.in
