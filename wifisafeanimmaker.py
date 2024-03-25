import os
import json

local_Path=os.getcwd()

#==================Bone List==================
Bone_List = {}
with open("bone_dictionary.txt") as f:
    for line in f:
       (key, val) = line.split()
       Bone_List[key]=val

#==================New Vis List==================
added_vis_List = {}
with open("added_vis.txt") as f:
    for line in f:
       (key, val) = line.split()
       added_vis_List[key]=val
#==================Settings List==================
settings_list= {}
with open("settings.txt") as f:
    for line in f:
       (key, pad, val) = line.split()
       settings_list[key]=val


vis_Prefix=settings_list["vis_prefix"]
exo_fix=int(settings_list["exo_fix"])
reference_animation=settings_list["reference_animation"]
exo_anchor_bone=settings_list["exo_anchor_bone"]
skip_vis=settings_list["skip_vis"]
use_prefix=settings_list["use_prefix"]

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
            
            vis_data=visMain(data, filename)
            
            print("(========================================================================Finished Modifying: "+filename)
            
            groupCount=len(trans_data["groups"])
            #print(groupCount)
            
            file_data = json.loads(data)
            if(trans_data["groups"][0]["group_type"]=="Visibility"):
                # Serializing json
                json_object = json.dumps(vis_data, indent=4)
                # Writing to sample.json
                with open(local_Path+'/OUT_JSON/'+filename, "w") as outfile:
                    outfile.write(json_object)
            elif(groupCount==1):
                # Serializing json
                json_object = json.dumps(trans_data, indent=4)
                # Writing to sample.json
                with open(local_Path+'/OUT_JSON/'+filename, "w") as outfile:
                    outfile.write(json_object)
            else:
                trans_data["groups"][1]=vis_data["groups"][1]
                # Serializing json
                json_object = json.dumps(trans_data, indent=4)
                # Writing to sample.json
                with open(local_Path+'/OUT_JSON/'+filename, "w") as outfile:
                    outfile.write(json_object)
   
    
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
    
    for bone in w_Trans:
        #print(bone["name"])
        
        try:
            print("[FOUND]: "+bone["name"]+" renaming to: "+Bone_List[bone["name"]])
            bone["name"]=Bone_List[bone["name"]]
        except:
            #print("[NOT FOUND]: "+bone["name"]+" not found in dictionary, removing")
            bone["name"]="NOMATCH"
    
    no_match_list=[]
    for idx, bone in enumerate(w_Trans):
        if bone["name"] == "NOMATCH":
            #w_Trans.pop(idx)
            #print("FOUND ONE at index: "+str(idx))
            no_match_list.append(idx)
            
    #print(no_match_list)
    for index in reversed(no_match_list):
        w_Trans.pop(index)

    
    if exo_fix==1:
        for bone in w_Trans:
            for frame in bone["tracks"][0]["values"]["Transform"]:
                if bone["name"]==exo_anchor_bone:
                        #print("Anchor")
                        continue
                else:
                    for match in file_ref["groups"][group_index]["nodes"]:
                        if match["name"]==bone["name"]:
                            frame["translation"]["x"]=[match][0]["tracks"][0]["values"]["Transform"][0]["translation"]["x"]
                            frame["translation"]["y"]=[match][0]["tracks"][0]["values"]["Transform"][0]["translation"]["y"]
                            frame["translation"]["z"]=[match][0]["tracks"][0]["values"]["Transform"][0]["translation"]["z"]
    
    combine_Trans = s_Trans + w_Trans
    
    file_data["groups"][group_index]["nodes"]=combine_Trans
    
    
    
 
    return file_data
    
#Copies every vismesh entry in Visibility group; renames duplicate entries to add prefix specified by vis_Prefix
def visMain(data, filename):
    print("[FUNCTION]: visMain")
    file_data = json.loads(data)
    file_copy = json.loads(data)
    
    
    text_file = open(reference_animation, "r")
    data = text_file.read()
    text_file.close()
    
    file_ref = json.loads(data)
    group_index=0
    groupCount=len(file_data["groups"])
    
    #print(skip_vis)
    if(skip_vis == "1"):
        print("[SKIPPED VIS]: Skip Vis is enabled, using vanilla entries")
        return file_data
    
    if(groupCount>1):
        if(file_data["groups"][0]["group_type"]=="Visibility"):
            print("[ANIM TYPE]: " + filename +" contains no motion data but has vis data")
            group_index=0
        elif(file_data["groups"][1]["group_type"]=="Visibility"):
            print("[ANIM TYPE]: " + filename +" contains motion and vis data")
            group_index=1
    else:
        if(file_data["groups"][0]["group_type"]!="Visibility"):
            print("[ANIM TYPE]: " + filename +" contains no vis data but has motion data")
            return file_data
        
    
    s_vis=file_data["groups"][group_index]["nodes"].copy()
    w_vis=file_copy["groups"][group_index]["nodes"].copy()
    
    if(use_prefix == "1"):
        for mesh in w_vis:
            print("[VIS ADD] added "+ vis_Prefix + mesh["name"])
            mesh["name"]=vis_Prefix+mesh["name"]
        
        for vanilla_mesh in s_vis:
            print("[TURN OFF] Vanilla vis mesh: " + str(vanilla_mesh["name"]))
            vanilla_mesh["tracks"]=[{"name":"Visibility","compensate_scale":False,"transform_flags":{"override_translation":False,"override_rotation":False,"override_scale":False,"override_compensate_scale":False},"values":{"Boolean":[False]}}]
    else:
        print("[SKIPPED PREFIX]: Using Vanilla vis mesh entries")
        
    for added_mesh in added_vis_List:
    
        #print(w_vis[0])
        if(added_vis_List[added_mesh]=="1"):
            w_vis.append({'name': added_mesh, "tracks":[{"name":"Visibility","compensate_scale":False,"transform_flags":{"override_translation":False,"override_rotation":False,"override_scale":False,"override_compensate_scale":False},"values":{"Boolean":[True]}}]})
        else:
            w_vis.append({'name': added_mesh, "tracks":[{"name":"Visibility","compensate_scale":False,"transform_flags":{"override_translation":False,"override_rotation":False,"override_scale":False,"override_compensate_scale":False},"values":{"Boolean":[False]}}]})
    
    if(use_prefix == "1"):
        combine_vis=s_vis + w_vis
    else:
        combine_vis=w_vis
        
    file_data["groups"][group_index]["nodes"]=combine_vis
    return file_data
    
    
main()