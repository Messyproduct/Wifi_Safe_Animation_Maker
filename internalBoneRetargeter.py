import os
import json

local_Path=os.getcwd()

#==================Settings List==================
settings_list= {}
with open("settings.txt") as f:
    for line in f:
       (key, pad, val) = line.split()
       settings_list[key]=val


vis_Prefix=settings_list["vis_prefix"]
exo_fix=1
reference_animation=settings_list["reference_animation"]
exo_anchor_bone=settings_list["exo_anchor_bone"]

#Contains all primary function calls
def main():
    print("[FUNCTION]: main")
    fileSpooler()
    
#Opens the Input folder and loops through every item
def fileSpooler():
    print("[FUNCTION]: fileSpooler")
    directory=local_Path+'/IN_JSON/'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            #print(filename)
            text_file = open(local_Path+"/IN_JSON/"+filename, "r")
            data = text_file.read()
            text_file.close()
            
            trans_data=transMain(data, filename)
            if(trans_data==0):
                continue
            
            print("(========================================================================Finished Modifying: "+filename)

            # Serializing json
            json_object = json.dumps(trans_data, indent=4)
            # Writing to sample.json
            with open(local_Path+'/OUT_JSON/'+filename, "w") as outfile:
                outfile.write(json_object)
   

    print("[FUNCTION]: retarget")
    file_data = json.loads(data)
    file_copy = json.loads(data)
    
    text_file = open(reference_animation, "r")
    data = text_file.read()
    text_file.close()
    
    if(file_data["groups"][0]["group_type"]=="Visibility"):
        print("[SKIP] "+ filename + " has no motion entry, skipping")
        return 0
    
    s_Trans=file_data["groups"][0]["nodes"].copy()
    

#    for bone in s_Trans:
#        for src, x in enumerate(Rename_List):
#            if(bone["name"]==Rename_List[x][0]):
#                print("[Found] " + bone["name"] +" matching bone " + Rename_List[x][0])
                
                
#                for target_bone in s_Trans:
#                    if(target_bone["name"]==Rename_List[x][1]):
#                        print("[Found] ...AND " + target_bone["name"] +" matches " + Rename_List[x][1])
#
#                        bone["tracks"][0]["values"]=target_bone["tracks"][0]["values"]
#                        #print(bone["tracks"][0]["values"]["Transform"][0]["translation"]["x"])
    
    json_object = json.dumps(file_data, indent=4)
    mod_data=json.loads(json_object)
    mod_Trans=mod_data["groups"][0]["nodes"].copy()
    
#    for src, x in enumerate(Rename_List):
#        for bone in mod_Trans:
#            if(bone["name"]==Rename_List[x][0]):
#                for frame in bone["tracks"][0]["values"]["Transform"]:
                    
#                    frame["translation"]["x"]=frame["translation"]["x"]+float(Rename_List[x][2])
    
    return mod_data
    
#Copies every bone entry in translation group; renames duplicate entries to use bone names in bone_list
def transMain(data, filename):
    print("[FUNCTION]: transMain")
    
    file_data = json.loads(data)
    file_copy = json.loads(data)
    
    
    text_file = open(reference_animation, "r")
    data = text_file.read()
    text_file.close()
    
    file_ref = json.loads(data)
    
    if(file_data["groups"][0]["group_type"]=="Visibility"):
        return file_data
    group_index=0

    #print(file_data["groups"][group_index]["nodes"][bone_index]["tracks"][0]["values"]["Transform"][frame_number][transform_type][transform_axis])
    
    s_Trans=file_data["groups"][group_index]["nodes"].copy()
    w_Trans=file_copy["groups"][group_index]["nodes"].copy()
    
#    for bone in w_Trans:
#        #print(bone["name"])
#        
#        try:
#            print("[FOUND]: "+bone["name"]+" renaming to: "+Bone_List[bone["name"]])
#            bone["name"]=Bone_List[bone["name"]]
#        except:
#            #print("[NOT FOUND]: "+bone["name"]+" not found in dictionary, removing")
#            bone["name"]="NOMATCH"
#    
#    no_match_list=[]
#    for idx, bone in enumerate(w_Trans):
#        if bone["name"] == "NOMATCH":
#            #w_Trans.pop(idx)
#            #print("FOUND ONE at index: "+str(idx))
#            no_match_list.append(idx)
#            
    #print(no_match_list)
#    for index in reversed(no_match_list):
#        w_Trans.pop(index)

    

    for bone in w_Trans:
        for frame in bone["tracks"][0]["values"]["Transform"]:
            if bone["name"]==exo_anchor_bone or bone["name"]=="Trans" or bone["name"]=="Rot":
                    #print("Anchor")
                    #print(bone["name"] + "matches special bone, skipping...")
                    continue
            else:
                for match in file_ref["groups"][group_index]["nodes"]:
                    #print([match][0]["tracks"][0]["values"]["Transform"][0]["translation"]["x"])
                    if match["name"]==bone["name"]:
                        frame["translation"]["x"]=[match][0]["tracks"][0]["values"]["Transform"][0]["translation"]["x"]
                        frame["translation"]["y"]=[match][0]["tracks"][0]["values"]["Transform"][0]["translation"]["y"]
                        frame["translation"]["z"]=[match][0]["tracks"][0]["values"]["Transform"][0]["translation"]["z"]
    
    combine_Trans = w_Trans
    
    file_data["groups"][group_index]["nodes"]=combine_Trans
    return file_data
    
    
main()