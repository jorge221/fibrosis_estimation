import os                           
import sys                          

from carputils import settings      
from carputils import tools         
from carputils import mesh          
from carputils import testing       


def parser():

    parser = tools.standard_parser()                                  
    group.add_argument('--duration',
        type=float, default=2500, 
        help='Duration of simulation (default is %(default)s ms)')
    group.add_argument('--IM',
        default='COURTEMANCHE',
        choices='COURTEMANCHE','koivumaki',
        help='pick ionic model to use (default is %(default)s)')
    group.add_argument('--catheter',
        default='', 
        help='Mesh with catheter geometry')
    
    return parser


def jobID(args):
    #================================
    #Generate name of top level output directory.
    #================================

    return 'patch_{}_{}_ms'.format(args.catheter, args.IM) 


@tools.carpexample(parser, jobID) 
def run(args, job):

    #================================
    #Number1: Defining the Geometry
    #================================

    meshname = args.catheter 


    #================================
    #Number2: Defining Ionic Model
    #================================

    if args.IM == 'COURTEMANCHE':

        imp_reg = ['-num_imp_regions', 1,
                    '-imp_region[0].im', "COURTEMANCHE",
                    '-imp_region[0].im_param', "g_CaL-55%,g_K1+100%,blf_i_Kur-50%,g_to-65%,g_Ks+100%,maxI_pCa+50%,maxI_NaCa+60%",
                    '-imp_region[0].name', "Tissue",
                    '-imp_region[0].num_IDs', 2,
                    '-imp_region[0].ID', {1,2}]
    else:
        imp_reg = ['-num_imp_regions', 1,
                    '-imp_region[0].im', "koivumaki",
                    '-imp_region[0].im_param', "cAF_lcell*1.10,gNa*0.82,g_Ca_L*0.41,g_t*0.38,g_sus*0.62,g_Ks*2.70,g_K1*1.62,k_NaCa*1.50,cAF_cpumps*0.84,cAF_RyR*2.00,PLB_SERCA_ratio*1.18,SLN_SERCA_ratio*0.60,base_phos*2.00",
                    '-imp_region[0].name', "Tissue",
                    '-imp_region[0].num_IDs', 2,
                    '-imp_region[0].ID', {1,2}]

    #======================================
    #Number3: Defining Tissue Conductivity
    #======================================

    g_reg = ['-num_gregions', 67,                
                 '-gregion[0].g_il', 0.1187,        #Cardiomyocytes utside the fibrotic area
                 '-gregion[0].g_it', 0.1187/2,            
                 '-gregion[0].g_in', 0.1187/3,             
                 '-gregion[0].g_el', 0.4262,       
                 '-gregion[0].g_et', 0.4262,            
                 '-gregion[0].g_en', 0.4262,              
                 '-gregion[0].num_IDs', 1,
                 '-gregion[0].ID', 1,

                 '-gregion[1].g_il', 0.1187,        #Cardiomycytes inside fibrotic area
                 '-gregion[1].g_it', 0.1187/2,            
                 '-gregion[1].g_in', 0.1187/3,             
                 '-gregion[1].g_el', 0.4262,       
                 '-gregion[1].g_et', 0.4262,            
                 '-gregion[1].g_en', 0.4262,              
                 '-gregion[1].num_IDs', 1,
                 '-gregion[1].ID', 1,

                 '-gregion[2].g_bath', 0.625,      #Extracellular medium
                 '-gregion[2].num_IDs', 1,
                 '-gregion[2].ID', 100,

                 '-gregion[3].g_bath', 1E-6,      #Collagen fibers
                 '-gregion[3].num_IDs', 1,
                 '-gregion[3].ID', 50,

                 '-gregion[4].g_bath', 1E-6,      #Catheter insulator
                 '-gregion[4].num_IDs', 1,
                 '-gregion[4].ID', 200]
    if args.catheter=='HDGRID':
        electrodes = []
    elif args.catheter ='LASSO':
        electrodes = []
    else:
        print('Catheter not yet implemented')
    
    g_vec = g_vec + electrodes


    #================================
    #Number4: Defining the Stimulus:
    #================================

    stim = ['-num_stim', 1,                               
            '-stimulus[0].stimtype', 0,                   
            '-stimulus[0].strength', 40.0,      #Strength of the stimulus in uA/cm^2
            '-stimulus[0].duration', 2.0,       #Duration of the stimulus in ms
            '-stimulus[0].start', 0,             #Start of the stimulation in ms
            '-stimulus[0].bcl', 600,             #Basic Cycle Length in ms
            '-stimulus[0].npls', 5,              #Number of pulses 
            '-stimulus[0].x0', 0,
            '-stimulus[0].xd', 310,
            '-stimulus[0].y0', 0,
            '-stimulus[0].yd', 50000,
            '-stimulus[0].z0', 1000,
            '-stimulus[0].zd', 2000,
            '-floating_ground',    1 ]


    #============================================
    #Number5: Defining the Mathmatical Solvers:
    #============================================

    # NUMERICAL PARAMETERS
    num_par = ['-dt', 10,        #usec 
               '-bidomain', 2]

    # I/O
    IO_par = ['-spacedt', 0.5,
              '-timedt',  10.0]

    #=====================================
    #Number6: Output everything to openCARP:
    #=====================================

    cmd = tools.carp_cmd()      #initialises cmd as a class that accepts valid opencarp inputs

    if args.catheter=='HDGRID':
        cmd += tools.gen_physics_opts(ExtraTags=[100,203,206,209,212,223,226,229,232,243,246,249,252,263,266,269,272,200,201,202,204,205,207,208,210,211,213,214,215,216,221,222,224,225,227,228,230,231,233,234,235,236,241,242,244,245,247,248,250,251,253,254,255,256,261,262,264,265,267,268,270,271,273,274,275,276], IntraTags=[1,2])
    elif args.catheter ='LASSO':
        cmd += tools.gen_physics_opts(ExtraTags=[100,203,206,209,212,223,226,229,232,243,246,249,252,263,266,269,272,200,201,202,204,205,207,208,210,211,213,214,215,216,221,222,224,225,227,228,230,231,233,234,235,236,241,242,244,245,247,248,250,251,253,254,255,256,261,262,264,265,267,268,270,271,273,274,275,276], IntraTags=[1,2])
    else:
        print('Catheter not yet implemented')


    cmd += imp_reg              #ionic model defined earlier
    cmd += g_reg                #conductivities of the regions we defined
    cmd += stim                 #stim definition based on coordinates
    cmd += num_par              #numerical solver parameters
    cmd += IO_par               #Output parameters
    simID = job.ID              #Name of our simulation

    
    cmd += ['-meshname', args.catheter,
            '-mass_lumping', 0,
            '-tend',     args.duration,
            '-gridout_i', 3,
            '-simID',    simID ]

    # Run simulation 
    job.carp(cmd)

if __name__ == '__main__':
    run()
