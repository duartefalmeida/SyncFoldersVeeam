import sys
import os
import shutil
import time


def sync(src, repl, log_file):
    """
    Synchronizes src and repl folders after the synchronization content of the
    repl folder will exactly match content of the src folder

    Arguments:
    src      - source folder path
    repl     - replica folder path
    log_file - file where replication/update/remove operations are logged

    """
    # List folders source and replica content or create empty folders them if they don't exist
    try:
        src_files = os.listdir(src)
    except FileNotFoundError:
        os.makedirs(src)
        src_files = os.listdir(src)
    except OSError as err:
        print(err)
        exit(0)
    try:
        repl_files = os.listdir(repl)
    except FileNotFoundError as err:
        os.makedirs(repl)
        repl_files = os.listdir(repl)
    except OSError as err:
        print(err)
        exit(0)

    src_files.sort()
    repl_files.sort()

    for src_fname in src_files:
        
        src_file_path = os.path.join(src,src_fname)
        repl_file_path = os.path.join(repl,src_fname)
        
        # Deals with sub folders recursively
        if os.path.isdir(src_file_path):
            sync(src_file_path, repl_file_path, log_file)
            continue
        
        # Updates a file or create if doesn't exist in replica folder
        try:
            if os.stat(src_file_path).st_mtime != os.stat(repl_file_path).st_mtime:
                
                shutil.copy2(src_file_path,repl_file_path, follow_symlinks=False)

                message = src_file_path + " has been updated into " + repl_file_path + '.'
                log_file.write(message + '\n')
                log_file.flush()
                print(message)
        
        except FileNotFoundError:
            try:
                shutil.copy2(src_file_path,repl_file_path, follow_symlinks=False)
            except OSError as err:
                print(err)
                exit(0)
            
            message = src_file_path + " has been replicated into " + repl_file_path + '.'
            log_file.write(message + '\n')
            log_file.flush()
            print(message)
                
        except OSError:
            
            try:
                shutil.copy2(src_file_path,repl_file_path, follow_symlinks=False)
            except OSError as err:
                print(err)
                exit(0)
            
            message = src_file_path + " has been replicated into " + repl_file_path + '.'
            log_file.write(message + '\n')
            log_file.flush()
            print(message)
        

            
    
    src_files = os.listdir(src)
    repl_files = os.listdir(repl)
    src_files.sort()
    repl_files.sort()

    # Removes a file from replica if it is not in source folder
    if len(src_files) < len(repl_files): 
        for repl_fname in repl_files:
            src_file_path = os.path.join(src,repl_fname)
            repl_file_path = os.path.join(repl,repl_fname)
            if not os.path.exists(src_file_path):
                if os.path.isdir(repl_file_path):
                    shutil.rmtree(repl_file_path)                    
                else:
                    os.unlink(repl_file_path)
                message = repl_file_path + " has been removed."
                log_file.write(message + '\n')
                log_file.flush()
                print(message)
                
    

if len(sys.argv) != 5:
    print("Usage: sync_folders.py <src_folder_path> <repl_folder_path> <sync_interval_in_sec> <log_file>")
    exit(0)

src = sys.argv[1]
repl = sys.argv[2]
sync_interval = sys.argv[3]
log_file = sys.argv[4]

try:
    sync_interval = int(sync_interval)
except ValueError:
    print("The sync interval should be an integer.")
    exit(0)

if not log_file.endswith(".txt"):
    print("Your log file should be a .txt file")
    exit(0)

f_log_file = open(log_file, 'w')
        
while True:
    sync(src, repl, f_log_file)    
    time.sleep(sync_interval)