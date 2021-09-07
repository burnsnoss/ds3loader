import sys
import os

save_filename = 'DS30000.sl2'
my_save_path = '/mnt/f/fake/path/for/github/'
levels = next(os.walk(my_save_path))[1]

def printInstructions():
    print 'you have call it like this: '
    print '\tpython ds3loader.py [save/load] [level_name/filename]'
    return

def throwError(code, custom_code = 0):
    print '\n'
    print 'Error ' + code
    if code == 0:
        print 'invalid number of arguments'
        printInstructions()
    elif code == 1:
        print '1st arg must be save or load'
        printInstructions()
    elif code == 2:
        print 'not a viable level'
        print 'viable levels include: '
        for lvl in levels:
            print '\t', lvl
    elif code == 3:
        print 'backup error: ' + custom_code
    elif code == 4: 
        print 'delete error: ' + custom_code
    elif code == 5:
        print 'copy error: ' + custom_code 
    elif code == 6:
        print 'save level names gotta be all letters sorry'
    elif code == 7: 
        print 'mkdir error: ' + custom_code
    else:
        print 'unknown error code.'
    exit()

def loadLevel(level_path, destination_path, bak_path):
    # make a backup
    backup_code = os.system('sudo cp -a ' + destination_path + ' ' + bak_path)
    if backup_code != 0:
        throwError(3, backup_code)

    # delete the file
    delete_code = os.system('sudo rm ' + destination_path)
    if delete_code != 0:
        throwError(4, delete_code)

    # copy custom save into game save location
    copy_code = os.system('sudo cp -a ' + level_path + ' ' + destination_path)
    if copy_code != 0:
        # undelete the file and error out
        os.system('sudo cp -a ' + bak_path + save_filename + ' ' + destination_path)
        throwError(5, copy_code)

    return

def saveLevel(save_path, level_path):
    # make the new level dir
    mkdir_code = os.system('sudo mkdir ' + level_path.strip(save_filename))
    if mkdir_code != 0:
        throwError(7, mkdir_code)

    # copy save to new folder
    copy_code = os.system('sudo cp -a ' + save_path + ' ' + level_path)
    if copy_code != 0:
        throwError(5, copy_code)

    return

if __name__ == "__main__":
    # error check and parse args
    if len(sys.argv) != 3:
        throwError(0)

    if sys.argv[1].strip().lower() == 'save':
        mode = 'save'
    elif sys.argv[1].strip().lower() == 'load':
        mode = 'load'
    else:
        throwError(1)

    level = sys.argv[2].strip().lower()

    custom_path = my_save_path + level + '/' + save_filename
    game_save_path = '/mnt/c/Users/fake/path/for/github/' + save_filename
    backup_path = '/mnt/c/Users/fake/path/for/github/'

    if mode == 'load':
        # make sure level is good
        if level not in levels: 
            throwError(2)
        loadLevel(custom_path, game_save_path, backup_path)

    if mode == 'save':
        # make sure the name of the new level is good
        if not level.isalpha():
            throwError(6)
        saveLevel(game_save_path, custom_path)

    print '\nnice, it worked. later\n'
    exit()

