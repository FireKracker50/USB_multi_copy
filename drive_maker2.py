import time
import os
import win32api

from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from shutil import disk_usage

print_lock = Lock()
_print = print


def main():
    drive_name = input('Enter a name for the drives. No Spaces: ')
    custom_dir = input("Input path to the source files: ")
    src_dir = (os.path.join(custom_dir))
    src_files = []  # list of files to be copied
    letters = []  # list to store drive letters

    for root, dirs, files in os.walk(src_dir):  # collects source files into list
        for file in files:
            source_file = os.path.normpath(file)
            src_files.append(source_file)
    while True:
        drive_letter = win32api.GetLogicalDriveStrings()  # Get drive letters from windows
        drive_letter = drive_letter.split('\000')[:-1]  # Format string of drive letter
        drives_to_format = []  # list of drive letters to be flashed
        for letter in drive_letter:  # collect drive letters to format
            if (disk_usage(letter)[0]) >= 64000000000:  # Change this number to adjust the removable drive cut-off size
                print("Drive {} over 64Gb detected and skipped".format(letter))
                pass
            else:
                letter = letter[:2]  # format string to match input of format and copy lines
                letters.append(letter)  # add drive letter to drive list
                drives_to_format.append(letter)

        with ThreadPoolExecutor(max_workers=20) as d:  # Multi-threaded drive formatting
            format_jobs = [d.submit(format_drives, drive_name, drive_to_format) for drive_to_format in letters]

        while any(format_job.running() for format_job in format_jobs):
            time.sleep(.1)

        with ThreadPoolExecutor(max_workers=20) as e:  # Multi-threaded file copying
            jobs = [e.submit(copy_file, src_dir, drive) for drive in drives_to_format]

        while any(job.running() for job in jobs):
            time.sleep(.1)

        print('done')

        runbool = input('Do you want to to run again with previous options? (y/n)')
        if runbool in ['y', 'Y', 'yes', 'YES', 'Yes']:
            drives_to_format.clear()
            drive_letter.clear()
            letters.clear()
            continue
        else:
            print("Good Bye")
            break

def print(*args, **kwargs):
    # Prevents concurrent printing.
    with print_lock:
        _print(*args, **kwargs)


def format_drives(drive_name1, drive):
    print('format drive {} with name {}.'.format(drive, drive_name1))
    os.system('format {} /FS:exFAT /Q /V:{} /y'.format(drive, drive_name1))  # Destructive part, Formats drives
    print('Format of drive {} completed.'.format(drive))


def copy_file(source_dir, dst_dir):
    print('starting transfer of {} to {}'.format(source_dir, dst_dir))
    os.system('xcopy "{}" "{}" /E'.format(source_dir, dst_dir))  # Copies files
    print('Transfer of files to {} completed'.format(dst_dir))
    

if __name__ == "__main__":
    main()
