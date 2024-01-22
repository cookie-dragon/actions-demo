#!/bin/bash

executable_filenames=( )

do_cython_executable() {
	local path=$1
	local executable_filenames=$2
	cd $path
	cython --embed -o ${executable_filenames}.c ${executable_filenames}.py
	${CROSS_COMPILE}gcc -O3 ${executable_filenames}.c -I /opt/Python-3.7.7/include/python3.7m -L /opt/Python-3.7.7/lib -lpython3.7m -o ${executable_filenames}
	rm -rf ${executable_filenames}.c
}

do_cython_so() {
	local path=$1
	local executable_filenames=$2
	cd $path
	cython -o ${executable_filenames}.c ${executable_filenames}.py

	${CROSS_COMPILE}gcc \
	-pthread \
	-DNDEBUG -g -fwrapv -O2 -Wall \
	-fno-strict-aliasing \
	-D_FORTIFY_SOURCE=2 \
	-g \
	-Wformat -Werror=format-security \
	-fPIC \
	-I/opt/Python-3.7.7/include/python3.7m \
	-c ${executable_filenames}.c \
	-o ${executable_filenames}.o

	${CROSS_COMPILE}gcc \
	-pthread \
	-DNDEBUG -g -fwrapv -O2 -Wall \
	-shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-z,relro \
	-Wstrict-prototypes \
	-fno-strict-aliasing \
	-D_FORTIFY_SOURCE=2 \
	-g \
	-Wformat -Werror=format-security \
	-fPIC \
	${executable_filenames}.o \
	-o ${executable_filenames}.so

	rm -rf ${executable_filenames}.c ${executable_filenames}.o
}

do_file() {
	local path=$1
	local filename=$2
	local relative_path=${path/$curr_dir\/$root_path/}
	local so_path=$curr_dir/$so_path$relative_path
	mkdir -p $so_path

	if [[ "${filename##*.}"x = "py"x ]] && [[ "${filename}" != "__init__.py" ]] && [[ "${filename}" != "setup.py" ]]; then
		filename_except_ext=${filename/.py/}
		if [[ ${executable_filenames[@]/${filename}/} != ${executable_filenames[@]} ]]; then
			do_cython_executable $path ${filename_except_ext}
			mv -f $path${filename_except_ext} $so_path
		else
			do_cython_so $path ${filename_except_ext}
			mv -f $path${filename_except_ext}.so $so_path
		fi
	else
		cp -rf $path$filename $so_path
	fi

}

loop_dir() {
	local path=$1
	for filename in `ls $path`
	do
		if [[ -f $path$filename ]]; then
			# echo $path$filename 是文件
			do_file $path $filename
		elif [[ -d $path$filename ]]; then
			# echo $path$filename 是目录
			loop_dir $path$filename/
		fi
	done
}

curr_dir=`pwd`
root_path=$1
if [[ ! "$root_path" =~ /$  ]]; then
	root_path=$root_path/
fi
so_path=so_$root_path
loop_dir $curr_dir/$root_path
