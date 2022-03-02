# USB_multi_copy
Mass Creation of USB drives, or Append files to bulk amount of USB devices

WARNING THIS PROGRAM IS DESTRUCTIVE TO DATA. IT WILL WIPE YOUR STORAGE DEVICES UNDER 64Gb
=========================================================================================

- Cody Greenwell
- cgreenwe@ford.com


This is a windows program to format, name and load removable drives.
--------------------------------------------------------------------

1. It asks for a name without spaces.
2. It asks for a location of the files and folders to be copied.
3. It formats the drives and names them. It checks for drives over 64Gb and skips them.
4. It then copies the files from a specified directory to all the drives.
5. It then asks if you want to perform the same action on a new set of drives with same files.

Requires
--------
pip install pywin32
