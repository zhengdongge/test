def analytical(file):
	symlist = []
	syms = os.popen('nm -C %s'%file).readlines()
	for sym in syms:
		index = sym.find('T')
		index1 = sym.find('(')
		index2 = sym.find(')')
		if index != -1 and index1 != -1 and index2 != -1:
			symlist.append(sym[index+2:])
	print(repr(symlist))
	return symlist

def analysis(sym):
	print(sym)
	index1 = sym.find('(')
	index2 = sym.find(')')
	argvdef = sym[index1+1:index2]
	while(1):
		index11 = argvdef.find('<')
		index22 = argvdef.find('>')
		if index11 != -1 and index22 != -1:
			argvdef = argvdef.replace(argvdef[index11:index22], '', 1)
		else:
			break
	return len(argvdef.split(',')), sym[:index1]


tstate = file.read()
for sym in symlist:
	len, func = analysis(sym)
	index1 = tstate.find('&&')
	index2 = tstate.find('&&', index1+2)
	argv = ''
	for i in range(len):
		argv += 'INT32 argv%d,' %i
	print(argv)
	tstate1 = tstate.replace(tstate[index1:index2+2], argv)
	function = ''
	for i in range(len):
		function += 'log << "argv%d" << %s << std::endl;\n'%(i, 'argv%d'%i)
	index1 = tstate.find('$$')
	index2 = tstate.find('$$', index1+2)
	print(function, tstate[index1:index2+2])
	tstate1 = tstate1.replace(tstate[index1:index2+3], function)
	insert = ''
	for i in range(len):
		insert += 'IARG_FUNCARG_CALLSITE_VALUE, %d,\n'%i
	index1 = tstate.find('**')
	index2 = tstate.find('**', index1+2)
	print(insert)
	tstate1 = tstate1.replace(tstate[index1:index2+3], insert)
	filename = '%ststate.cpp'%func
	print(filename)
	tstatefile = open(filename, 'w')
	tstatefile.write(tstate1)
	tstatefile.close()

	