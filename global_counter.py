# $language = "python"
# $interface = "1.0"

def main():

	import re
	import time
	import datetime

	#test it print system path for python libs
	#import sys
	#import os
	#crt.Dialog.MessageBox(str(sys.path))

	# Here is where we will set the value of the string that will indicate that
	# we have reached the end of the data that we wanted capture with the
	# ReadString method.
	szPromptEn			= "> "
	szPromptConf		= "# "
	
	#Commands
	szCmdCliSetMode		= "set cli config-output-format set"
	szCmdCliPagerOff	= "set cli pager off"
	szCmdEnter			= "\r\n"
	szCmdGlCntChkErr	= "show counter global filter delta yes | match error"
	szCmdGlCntChkDrp	= "show counter global filter delta yes | match drop"
	szOutput 			= "Datetime,CounterName,Value\r\n"

	# Using GetScriptTab() will make this script 'tab safe' in that all of the
	# script's functionality will be carried out on the correct tab. From here
	# on out we'll use the objTab object instead of the crt object.
	objTab = crt.GetScriptTab()
	
	# Check if remote host is connected
	if objTab.Session.Connected != True:
		crt.Dialog.MessageBox(
		"Error.\n" +
		"This script was designed to be launched after a valid "+
		"connection is established.\n\n"+
		"Please connect to a remote machine before running this script.")
		return

	# Ensure that we don't "miss" data coming from the remote by setting
	# our Screen's Synchronous flag to true.
	objTab.Screen.Synchronous = True
	
	# Instruct WaitForString and ReadString to ignore escape sequences when
	# detecting and capturing data received from the remote (this doesn't
	# affect the way the data is displayed to the screen, only how it is handled
	# by the WaitForString, WaitForStrings, and ReadString methods associated
	# with the Screen object.
	objTab.Screen.IgnoreEscape = True

	# Prompt for a count number
	#
	CntNr = crt.Dialog.Prompt("Enter the number of times the counters should be collected:","Define number of times", "", False)
	if CntNr == "" :
		crt.Dialog.MessageBox("Error.\nThe number of times is a required field!")
		return
	
	CntNr = CntNr.lstrip()
	CntNr = CntNr.rstrip()
	CntNr = CntNr.lower()
	
	# Prompt for a sleep time in seconds
	#
	szSlTime = crt.Dialog.Prompt("Enter the time period between 2 commands [seconds]:","Define the time period", "", False)
	if szSlTime == "" :
		crt.Dialog.MessageBox("Error.\n number for sleep time is a required field!")
		return
	
	szSlTime = szSlTime.lstrip()
	szSlTime = szSlTime.rstrip()
	szSlTime = szSlTime.lower()
	
	# Update the prompt var
	objTab.Screen.Send(szCmdEnter)
	objTab.Screen.WaitForString(szPromptEn)
	szPromptEn1 = objTab.Screen.ReadString(szPromptEn)
	szPromptEn1 = szPromptEn1.lstrip()
	szPromptEn1 = szPromptEn1.rstrip()
	szPromptEn = szPromptEn1 + szPromptEn
	
	# We begin the process by sending the commands.
	objTab.Screen.Send(szCmdCliSetMode + "\r\n")
	objTab.Screen.WaitForString(szPromptEn + szCmdCliSetMode + "\r\n")
	objTab.Screen.Send(szCmdCliPagerOff + "\r\n")
	objTab.Screen.WaitForString(szPromptEn + szCmdCliPagerOff + "\r\n")
	
	while (CntNr > 0):

		t = datetime.datetime.now()
		mytime = t.strftime('%m/%d/%Y-%H:%M:%S')
	
		objTab.Screen.Send(szCmdGlCntChkErr + "\r\n")
		# Wait for the command and the trailing CR to be echoed back from the remote
		# before we start capturing data... Otherwise, we'll capture the command we
		# issued, as well as the results, and in this example, we only want to
		# capture the results.
		objTab.Screen.WaitForString(szPromptEn + szCmdGlCntChkErr + "\r\n")

		# This will cause ReadString() to capture data until we see the szPromptEn
		# value.
		szResult = objTab.Screen.ReadString(szPromptEn)
		
		objTab.Screen.Send(szCmdGlCntChkDrp + "\r\n")
		# Wait for the command and the trailing CR to be echoed back from the remote
		# before we start capturing data... Otherwise, we'll capture the command we
		# issued, as well as the results, and in this example, we only want to
		# capture the results.
		objTab.Screen.WaitForString(szPromptEn + szCmdGlCntChkDrp + "\r\n")

		# This will cause ReadString() to capture data until we see the szPromptEn
		# value.
		szResult += objTab.Screen.ReadString(szPromptEn)
			
		for line in szResult.splitlines():
			line2 = line.split()
			# line2[0] name of the counter
			# line2[1] counter value
			# str(mytime) datetime
			szOutput += str(mytime) + "," + line2[0] + "," + line2[1] + "\r\n"
		
		CntNr = int(CntNr) - 1
		time.sleep(int(szSlTime)) # delays for defined seconds
	
	crt.Clipboard.Text = szOutput
	crt.Dialog.MessageBox("Done!the output is on your clipboard! In excel do import-pivot-chart! ")
main()