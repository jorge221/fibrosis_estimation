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
    #Generate name of top level output directory
    #================================

    return 'patch_{}_{}'.format(args.catheter, args.IM) 


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
        electrodes = [202,206,210,214,222,226,230,234,242,246,250,254,262,266,270,274]
    elif args.catheter ='LASSO':
        electrodes = [204,207,214,217,224,227,234,237,244,247,254,257,264,267,274,277,284,287,294,297]
    else:
        print('Catheter not yet implemented')

    g_elec = ['-gregion[5].g_bath', 1E6,      #Electrodes
              '-gregion[5].num_IDs', len(electrodes),
              '-gregion[5].ID', electrode]
        
    g_reg = g_reg + g_elec

    #================================
    #Number4: Defining the Stimulus
    #================================

    stim = ['-num_stim', 1,                               
            '-stimulus[0].stimtype', 0,                   
            '-stimulus[0].strength', 40.0,      #Strength of the stimulus in uA/cm^2
            '-stimulus[0].duration', 2.0,       #Duration of the stimulus in ms
            '-stimulus[0].start', 0,             #Start of the stimulation in ms
            '-stimulus[0].bcl', 600,             #Basic Cycle Length in ms
            '-stimulus[0].npls', 5]              #Number of pulses 
    
    if args.location == 'left':
        sitm_reg = ['-stimulus[0].x0', 0,
            '-stimulus[0].xd', 310,
            '-stimulus[0].y0', 0,
            '-stimulus[0].yd', 50000,
            '-stimulus[0].z0', 1000,
            '-stimulus[0].zd', 2000 ]
    elif args.location=='bottom':
        sitm_reg = ['-stimulus[0].x0', 0,
                    '-stimulus[0].xd', 50000,
                    '-stimulus[0].y0', 0,
                    '-stimulus[0].yd', 310,
                    '-stimulus[0].z0', 1000,
                    '-stimulus[0].zd', 2000 ]
    elif args.locatio=='leftcorner':
        sitm_reg = ['-stimulus[0].x0', 29700,
                    '-stimulus[0].xd', 300,
                    '-stimulus[0].y0', 29700,
                    '-stimulus[0].yd', 300,
                    '-stimulus[0].z0', 1000,
                    '-stimulus[0].zd', 2000 ]
    else:
        print('Location not yet implemented')

    stim = stim + stim_reg

    #============================================
    #Number5: Defining the Mathmatical Solvers
    #============================================

    # NUMERICAL PARAMETERS
    num_par = ['-dt', 10,        #usec 
               '-bidomain', 2,
               '-mass_lumping', 0]

    # I/O
    IO_par = ['-spacedt', 0.5,
              '-timedt',  10.0,
              '-gridout_i', 3]  #Outputs the intracellular grid

    #=====================================
    #Number6: Output everything to openCARP
    #=====================================

    cmd = tools.carp_cmd()      #Initialises cmd as a class that accepts valid opencarp inputs

    cmd += tools.gen_physics_opts(ExtraTags=[50,100,200] + electrodes, IntraTags=[1,2]) #Define physical regions

    cmd += imp_reg              #Ionic model defined earlier
    cmd += g_reg                #Conductivities of the regions we defined
    cmd += stim                 #Stim definition based on coordinates
    cmd += num_par              #Numerical solver parameters
    cmd += IO_par               #Output parameters
    simID = job.ID              #Name of our simulation
    
    cmd += ['-meshname', meshname,
            '-tend', args.duration,
            '-simID', simID ]

    # Run simulation 
    job.carp(cmd)

if __name__ == '__main__':
    run()
