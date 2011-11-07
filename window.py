# Rewin - resize your windows with keyboard shortcuts
# Author - Vaidik Kapoor <kapoor.vaidik@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Main python script for Rewin

import os, re
from subprocess import Popen, PIPE, STDOUT

def getWindowId():
	process = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	response = process.communicate()

	exp = re.compile('[0-9]x[0-9]+')
	result = exp.findall(response[0])
	'''result = response'''
	
	return result[0]

def horizontal_max():
	process = Popen(['wmctrl', '-v', '-r', ':ACTIVE:', '-b', 'add,maximized_horz'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = process.communicate()

def vertical_max():
	process = Popen(['wmctrl', '-v', '-r', ':ACTIVE:', '-b', 'add,maximized_vert'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = process.communicate()

def left_half(width, height, y):
	a = Popen(['wmctrl -v -r :ACTIVE: -b "remove,maximized_horz,maximized_vert"'], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = a.communicate()

	cmd = 'wmctrl -v -r :ACTIVE: -e 0,0,%s,%s,%s' % (y,(width/2),height)
	a = Popen([cmd], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = a.communicate()

def right_half(width, height, y):
	a = Popen(['wmctrl -v -r :ACTIVE: -b "remove,maximized_horz,maximized_vert"'], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = a.communicate()

	cmd = 'wmctrl -v -r :ACTIVE: -e 0,%s,%s,%s,%s' % ((width/2),y,(width/2),height)
	a = Popen([cmd], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = a.communicate()

def upper_half(x,width,height):
	a = Popen(['wmctrl -v -r :ACTIVE: -b "remove,maximized_horz,maximized_vert"'], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  result = a.communicate()

  cmd = 'wmctrl -v -r :ACTIVE: -e 0,%s,0,%s,%s' % (x,width,(height/2))
  a = Popen([cmd], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  result = a.communicate()

def lower_half(x,width,height):
  a = Popen(['wmctrl -v -r :ACTIVE: -b "remove,maximized_horz,maximized_vert"'], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  result = a.communicate()

  cmd = 'wmctrl -v -r :ACTIVE: -e 0,%s,%s,%s,%s' % (x,(height/2),width,(height/2))
  a = Popen([cmd], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  result = a.communicate()

def get_screen_res():
	a=Popen(['xrandr | grep "*"'], shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = a.communicate()
	result = result[0]
	exp = re.compile('[0-9]*x[0-9]*')
	result = exp.findall(result)
	result = result[0].split('x')
	return eval(result[0]), eval(result[1])

def main():
	return 0

if __name__ == "__main__":
	wid = getWindowId()

	'''
	process = Popen(['zenity', '--info', '--text', wid], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	'''

	pid = Popen(['wmctrl', '-l', '-G', '-p'], stdout=PIPE)
	result=pid.communicate()

	result=result[0].split('\n')

	regex = re.compile('[0-9]x[0-9]+')
	for row in result:
		row_wid = regex.findall(row)
		if len(row_wid) != 0:
			row_wid = row_wid[0]
		else:
			row_wid = ''

		if len(row_wid) == 10:
			row_wid = row_wid.replace('x0', 'x')
		
		if row_wid == wid:
			print 'Row: %s' % row
			wid_row = row

	regex = re.compile('[0-9][0-9]*')
	wid_row_arr = regex.findall(wid_row)
	x = eval(wid_row_arr[4])
	y = eval(wid_row_arr[5])
	w = eval(wid_row_arr[6])
	h = eval(wid_row_arr[7])

	y = (y/2) + 1

	horizontal_max()
	screen_width, screen_height = get_screen_res()
	left_half(screen_width, h, y)

	main()
