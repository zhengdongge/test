VOID funcbefore(CHAR *rtnname, &&INT32&&){
	$$std::cout << rtnname << std::endl;$$
}

VOID funcafter(CHAR *rtnname, int ret){
	std::cout << rtnname << std::endl;
}