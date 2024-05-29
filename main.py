
import smb.SMBConnection 
import io


def smbwalk(share_name):
    

    share_dict = dict() #{"/":[]}

    not_done_list = ['/']

    while len(not_done_list) > 0:

        curr_dir_name = not_done_list[0]

        entry_list = conn.listPath(share_name, curr_dir_name)

        share_dict[curr_dir_name] = entry_list

        for entry in entry_list:
            if entry.isDirectory and entry.filename not in ['.','..']:
                if curr_dir_name == '/':  not_done_list.append(curr_dir_name  + entry.filename)
                else: not_done_list.append(curr_dir_name + '/' + entry.filename)
        
        not_done_list.pop(0)

    return share_dict


userID = '' # change this
password = '' # change this
client_machine_name = 'name' # think a bit about this
server_name = '' # think a bit about this

# 1 more below

conn = smb.SMBConnection.SMBConnection(userID, password, client_machine_name, server_name, use_ntlm_v2 = True)


conn.connect("127.0.0.1", 445) # change this

print(conn)
Response = conn.listShares(timeout=30)



share_list = []

for i in Response:
    if i.name != "IPC$":
        share_list.append(i)


share_dict_dict = dict()

for share in share_list:


    print(share.name)
    share_dict = smbwalk(share.name)

    share_dict_dict[share.name] = share_dict



keyword_list = ['pass','cred','hash'] # can easily adjust functionality with this

CONF_context_before = 1 # context like grep -B
CONF_context_after = 1 # context like grep -A

for key in share_dict_dict.keys():

    share_dict = share_dict_dict[key]

    for key2 in share_dict.keys():
        dir_list = share_dict[key2]

        for entry in dir_list:
            if any( [x in entry.filename for x in keyword_list] ):
                if key2 == '/': print(key+"/"+entry.filename, 'dir:',entry.isDirectory)
                else: print(key+"/"+key2+"/"+entry.filename, 'dir:',entry.isDirectory)

            if not entry.isDirectory:

                with io.BytesIO() as interface:

                    path = key2 + '/'+ entry.filename
                    if key2 == '/': path = '/' + entry.filename

                    attr, length = conn.retrieveFile(key,path,interface)
                    
                    if length < 1024**3:

                        found = False

                        lines = interface.getvalue().split(b'\n')

                        #print(length, lines)
                        
                        for i, line in enumerate(lines):
                            line = line.decode().lower()
                            #print(line)
                            if any( [x in line for x in keyword_list] ):
                                
                                if not found: 
                                    print(key+path, 'dir:',entry.isDirectory)
                                    found = True
                                [print(y) for y in [ x.decode() for x in lines[i-CONF_context_before:i+1+CONF_context_after] ] ]

                            
                        try:
                            None

                        except:
                            None
                









    




#def scan():

    





