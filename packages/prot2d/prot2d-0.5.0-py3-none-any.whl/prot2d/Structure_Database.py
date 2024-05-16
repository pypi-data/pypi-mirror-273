import numpy as np
import subprocess
import pandas as pd
import importlib.resources as pkg_resources
import csv


#SCOP_summary = '/Users/constantincarl/Uni/BachelorThesis/prot2D/database/SCOP_SF_summary.txt'
class Structure_Database:
    # the obj is created using at least foldseek_executable path and tmp_Dir from the user.
    # db information and data is saved in the package structure itself (default relative paths)
    # --> the data base can be acce
    def __init__(self,foldseek_executable,tmp_dir):
        self.foldseek_executable = foldseek_executable
        self.tmp_dir = tmp_dir
        self.presetSCOPdb = 'prot2d.SF_database'
        self.SCOP_SF_db_info_tsv = self.load_package_file(self.presetSCOPdb,'db_info.tsv') #SCOP SF info tsv
        self.foldseek_SCOP_db= self.load_package_file(self.presetSCOPdb+'.foldseek_db','db') #SCOP SF database dir
        
        self.flexUSERdb = 'prot2d.flexUSER_database'
        self.USER_db_info_tsv = self.load_package_file(self.flexUSERdb,'db_info.tsv') #SCOP SF info tsv
        self.foldseek_USER_db= self.load_package_file(self.flexUSERdb+'.foldseek_db','db') #SCOP SF database dir

    def load_package_file(self,package_data_dir,filename):
        with pkg_resources.path(package_data_dir,filename) as path:
            return path
    
    def create_USER_PDB_foldseek_index(self,pdb_dir):
        # create foldseek index out of user_pdbs 
        command = [self.foldseek_executable,'createdb',pdb_dir,self.foldseek_USER_db]
        subprocess.run(command)
        # TODO: important: delete not working pdbs from db_info table --> else errors

    def check_create_USERdb_info_table(self,name_id_mapping, db_info_table):
        id_name_dict = {}
        # Check uniqueness of IDs and names
        with open(name_id_mapping, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["ID"] in id_name_dict:
                    print(f"Duplicate ID found: {row['ID']}")
                    return None
                if row["NAME"] in id_name_dict.values():
                    print(f"Duplicate NAME found: {row['NAME']}")
                    return None
                id_name_dict[row["ID"]] = row["NAME"]
        # create db_info_table with rotation matrix init
        with open(db_info_table, "w") as file:
            file.write("ID\trepresentative\trotation_matrix\trotation_type\n")
            for id, representative in id_name_dict.items():
                line = f"{id}\t{representative}\t(1, 0, 0, 0, 1, 0, 0, 0, 1)\tautomatic\n"
                file.write(line)
        print("Database info TSV was created successfully.")
        return db_info_table

    def create_fixed_tmp_db(self,sf_number):
        #not used !
        db  = pd.read_csv(self.SCOP_SF_db_info_tsv, sep='\t')
        if sf_number not in db['SF'].values:
                print(f"{sf_number} is not a valid SCOP SF number")
                return False
        else:
            filtered_row = db.loc[db['SF'] == sf_number]
            representative = filtered_row['representative']

    def get_matching_SF_U_T_fixed_region(self,input_pdb, min_prob,fixed_sf_number = None, use_flex_USER_db=False):
        db = self.foldseek_SCOP_db if not use_flex_USER_db else self.foldseek_USER_db 
        db_info = self.SCOP_SF_db_info_tsv if not use_flex_USER_db else self.USER_db_info_tsv
        #TODO: change naming from sf to id...
        #TODO: check if user db is correctly set for usage (db info file available...?!)
        try:
            filename = input_pdb.split('/')[-1]  # Gets the filename with extension
            filename_without_ext = '.'.join(filename.split('.')[:-1])
            result_file = self.tmp_dir+'/'+filename_without_ext+'_foldseek_result'
            print_file = self.tmp_dir+'/'+filename_without_ext+'foldseek_printOut'
            command = [self.foldseek_executable,'easy-search', input_pdb,db,result_file , self.tmp_dir,'--format-output', 'query,target,qstart,qend,tstart,tend,tseq,prob,alntmscore,u,t,lddtfull,qaln,taln']
            print("### foldseek start ### ")
            with open(print_file, 'w') as output_file:
                subprocess.run(command,stdout=output_file, stderr=output_file)

            column_names = ['query', 'target', 'qstart', 'qend', 'tstart', 'tend', 'tseq', 'prob', 'alntmscore', 'u', 't','lddtfull','qaln','taln']
            df = pd.read_csv(result_file, sep='\t', names=column_names)
            if len(df) ==0:
                print("No matching SF found")
                return None,None,None,None,None,None,None
            if fixed_sf_number!=None:
                try:
                    fam_info  = pd.read_csv(db_info, sep='\t')
                    if fixed_sf_number not in fam_info['SF'].values:
                        raise ValueError(f"Error: {fixed_sf_number} is not a valid SCOP SF number")
                    sf_row = fam_info.loc[fam_info['SF'] == fixed_sf_number]
                    fixed_representative_name = sf_row['representative'].iloc[0]
                    try:
                        matched_row = df[df['target'] == fixed_representative_name+".pdb"].iloc[0]
                        print(f"Using fixed SF: {fixed_sf_number} (representative: {fixed_representative_name})")
                    except:
                        raise ValueError(f"Error: The given SF ({fixed_sf_number}) was not found in the FoldSeek result file (to distant to input or not valid).")
                except Exception as e:
                    print("\033[91m" + f"\nError: {str(e)}")
                    print("Match with highest prob will be used!\n"+"\033[0m")
                    matched_row = df.loc[df['prob'].idxmax()]
            else:
                matched_row=df.loc[df['prob'].idxmax()]
                if matched_row['prob']< min_prob:
                    print(f"No matching SF with prob > {min_prob} found (highest prob: {matched_row['prob']})")
                    return None,None,None,None,None,None,None
            best_SF_representative = matched_row['target'].replace('.pdb','')
            prob = matched_row['prob']
            u = matched_row['u']
            t = matched_row['t']
            q_start = matched_row['qstart']
            q_end = matched_row['qend']
            t_start = matched_row['tstart']
            t_end = matched_row['tend']
            lddtfull= matched_row['lddtfull'].split(',')
        
            qaln=matched_row['qaln']
            print(f"query-aln: {qaln}")
            taln= matched_row['taln']
            print(f"target-aln: {taln}")
            print("### foldseek finished ###")

            new_lddtfull = []
            lddt_index = 0
            len(qaln.replace('-',''))
            len(taln.replace('-',''))
            for q_char, t_char in zip(qaln, taln):
                if t_char == '-':
                    #additional residue in input protein
                    new_lddtfull.append(0)
                elif q_char != '-' and t_char != '-':
                    #alignment residue with existing lddt
                    new_lddtfull.append(lddtfull[lddt_index])
                    lddt_index += 1

            ## read in SCOP_db summary file ##
            df = pd.read_csv(db_info, sep='\t')
            df.replace({'None': None, 'nan': None}, inplace=True)

            specific_row = df.loc[df['representative'] == best_SF_representative]
            if not df['representative'].eq(best_SF_representative).any():
                print("db error !!!!! (representative in db not in summary file)")
                return None,None,None,None,None,None,None
            ID = specific_row['ID'].iloc[0]
            fixed_rot_matrix_string = specific_row['rotation_matrix'].iloc[0]
            
            fixed_rot =string_matrix_to_numpy(fixed_rot_matrix_string)
            u_matrix = np.array([float(num) for num in u.split(',')]).reshape(3, 3)
            t_vector = np.array([float(num) for num in t.split(',')])
            
            print(f"\n################# foldseek result  (user_db: {use_flex_USER_db})")
            print("--- Rotating by inital SF FoldSeek alignment + fixed family rotation ---")
            print(f"input: {filename_without_ext}")
            print(f"ID: {ID} (prob: {matched_row['prob']})")
            print(f"representative: {best_SF_representative}")
            print("#################\n")
            
            return ID,prob,u_matrix,t_vector,fixed_rot,(q_start,q_end),new_lddtfull
        except Exception as e:
            print(e)
            return None,None,None,None,None,None,None

    def initial_and_fixed_Sf_rot_region(self,input_pdb,drop_family_prob,fixed_sf, flex_USER_db):
        sf,prob,u,t,fixed_rot,aligned_region,lddtfull = self.get_matching_SF_U_T_fixed_region(input_pdb,drop_family_prob,fixed_sf,flex_USER_db)
        if sf == None:
            return None,None,None,None,None
        U_inv,T_inv = invert_UT(u,t)

        filename = input_pdb.split('/')[-1]  # Gets the filename with extension
        filename_without_ext = '.'.join(filename.split('.')[:-1])
        sf_aligned_rot_pdb = self.tmp_dir+'/'+filename_without_ext+f'_sf-{sf}_aligned_rot.pdb'
        sf_fixed_rot_pdb = self.tmp_dir+'/'+filename_without_ext+f'_sf-{sf}_fixed_rot.pdb'
        empty_t = np.array([0,0,0])
        transform_pdb(input_pdb,sf_aligned_rot_pdb,U_inv,T_inv)
        transform_pdb(sf_aligned_rot_pdb,sf_fixed_rot_pdb,fixed_rot,empty_t)
        return sf,prob,sf_fixed_rot_pdb,aligned_region,lddtfull

    def init_db_from_summary_file(SCOP_summary_file,db_outfile):
        init_matrix= np.array([
        [1,0,0],
        [0,1,0],    
        [0,0,1]
        ])
        summary = pd.read_csv(SCOP_summary_file, sep='\t', na_values=['None', 'nan'])
        summary['rotation_matrix'] = [numpy_matrix_to_string(init_matrix)] * len(summary)
        summary['rotation_type'] = ['automatic'] * len(summary)

        summary.to_csv(db_outfile, sep='\t', index=False)

    def set_manual_SF_rotation(self,SF_number, numpy_rotatoin_matrix, manual=True):
        if not isinstance(numpy_rotatoin_matrix, np.ndarray) or numpy_rotatoin_matrix.shape != (3, 3):
            print("ERROR: Wrong rotation matrix format (numpy 3x3 needed)!")
            print('example:')
            print( np.array([
        [1,0,0],
        [0,1,0],    
        [0,0,1]
        ]))
            return False
        
        db  = pd.read_csv(self.SCOP_SF_db_info_tsv, sep='\t')

        if SF_number not in db['SF'].values:
            print(f"{SF_number} is not a valid SCOP SF number")
            return False
        
        db.loc[db['SF'] == SF_number, 'rotation_matrix'] = numpy_matrix_to_string(numpy_rotatoin_matrix)
        if manual:
            db.loc[db['SF'] == SF_number, 'rotation_type'] = 'manual'
        db.to_csv(self.SCOP_SF_db_info_tsv, sep='\t', index=False)
        print(f"Successfully changed fixed rotation for SF: {SF_number} to {numpy_rotatoin_matrix}")
        return True
    
    def get_SF_info(self,sf_number:int):
        """
        user can input a SCOP SF and get information on the representative etc
        """
        db  = pd.read_csv(self.SCOP_SF_db_info_tsv, sep='\t')
        if sf_number not in db['SF'].values:
                print(f"{sf_number} is not a valid SCOP SF number")
                return False
        else:
            filtered_row = db.loc[db['SF'] == sf_number]
            print(filtered_row)
            return filtered_row
    
def transform_pymol_out_to_UT(get_view_output):
    pymol_matrix_string = get_view_output.replace("(", "").replace(")", "")
    pymol_number_list = [float(num) for num in pymol_matrix_string.split(",")]

    rotation_matrix = np.array(pymol_number_list[:9]).reshape((3, 3), order='F')
    translation_vector = np.array([0, 0, 0]) # no linear object shifting
    return rotation_matrix,translation_vector

def string_matrix_to_numpy(matrix_string):
        number_strings = matrix_string.strip("()").split(",")
        number_floats = [float(num) for num in number_strings]
        matrix = np.array(number_floats).reshape(3, 3)
        return matrix

def numpy_matrix_to_string(matrix):
    matrix_string = ', '.join(map(str, matrix.flatten()))
    return '('+matrix_string+')'

def transform_pdb(pdb_file, output_file, U,T):

    with open(pdb_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as out:
        for line in lines:
            if line.startswith(('ATOM', 'HETATM')):
                # Umwandeln der Koordinaten in Fließkommazahlen
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                # Transformation anwenden
                x_new, y_new, z_new = U @ (np.array([x, y, z]) + T)

                # Zeile mit neuen Koordinaten schreiben
                out.write(f"{line[:30]:<30}{x_new:8.3f}{y_new:8.3f}{z_new:8.3f}{line[54:]}")
            else:
                out.write(line)

def invert_UT (U,T):
    U_inv = np.transpose(U)
    T_inv = -T
    return U_inv,T_inv



