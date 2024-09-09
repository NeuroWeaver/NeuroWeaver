#!/bin/bash

export CLASSPATH=".:/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH"

# antlr4 aliases
alias antlr='java -Xmx500M -cp "/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
alias grun='java -Xmx500M -cp "/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'

function antlr_java {
    if [ -z "$1" ]
    then
	echo [ERROR] You must provide .g file!
	return 1
    else
	local grammar_file=$1
    fi

    antlr $grammaer_file
}

function antlr_python {
    if [ -z "$1" ]
    then
	echo [ERROR] You must provide .g file!
	return 1
    else
	local grammar_file=$1
    fi

    antlr -Dlanguage=Python3 $grammaer_file
}

function run_antlr {
    while getopts ":t:" opt;
    do
	case $opt in
	    t)
		echo "$OPTARG"
		if [ "$OPTARG" == "add" ]
		then
		    echo [INFO] Generating grammar for abstract domain definition...
		    target_abstract_domain
		    return 0
		elif [ "$OPTARG" == "esl" ]
		then
		    echo [INFO] Generating grammar for engine specification language...
		    target_engine_spec_lang
		    return 0
		else
		    echo [ERROR] "Invalid option: -$OPTARG" >&2
		    return 1
		fi
		;;
	    :)
		echo [ERROR] "Option -$OPTARG requires an argument." >&2
		return 1
		;;
	esac
    done

    target_abstract_domain
    target_engine_spec_lang
}

function target_abstract_domain {
    local rootdir=~/ohai.src/esa/grammar/abstract_domain
    if [ ! -d ${rootdir} ]
    then
	echo mkdir ${rootdir}
	mkdir ${rootdir}
	touch ${rootdir}/__init__.py
    fi

    local pythondir=${rootdir}/python
    if [ ! -d ${pythondir} ]
    then
	echo mkdir ${pythondir}
	mkdir ${pythondir}
	touch ${pythondir}/__init__.py
    fi

    local javadir=${rootdir}/java
    if [ ! -d ${javadir} ]
    then
	echo mkdir ${javadir}
	mkdir ${javadir}
    fi

    local grammar_file=AbstractDomain.g
    antlr -Dlanguage=Python3 ${rootdir}/${grammar_file} -o ${pythondir}
    antlr ${rootdir}/${grammar_file} -o ${javadir}

    local java_build=${javadir}/build
    if [ ! -d ${java_build} ]
    then
	mkdir ${java_build}
    fi

    javac ${javadir}/*.java -d ${java_build}
}

function target_engine_spec_lang {
    local rootdir=~/ohai.src/esa/grammar/engine_spec_lang
    if [ ! -d ${rootdir} ]
    then
	echo mkdir ${rootdir}
	mkdir ${rootdir}
	if [ ! -f ${rootdir}/__init__.py ]
	then
	    touch ${rootdir}/__init__.py
	fi
    fi

    local pythondir=${rootdir}/python
    if [ ! -d ${pythondir} ]
    then
	echo mkdir ${pythondir}
	mkdir ${pythondir}
	touch ${pythondir}/__init__.py
    fi

    local javadir=${rootdir}/java
    if [ ! -d ${javadir} ]
    then
	echo mkdir ${javadir}
	mkdir ${javadir}
    fi

    local grammar_file=Esl.g
    antlr -Dlanguage=Python3 ${rootdir}/${grammar_file} -o ${pythondir}
    antlr ${rootdir}/${grammar_file} -o ${javadir}

    local java_build=${javadir}/build
    if [ ! -d ${java_build} ]
    then
	mkdir ${java_build}
    fi

    javac ${javadir}/*.java -d ${java_build}
}

function show_ast {
    if [ -z "$1" ]
    then
	echo "Usage: show_ast [domain | engine] [.domain file | .engine file (optional)]"
	return 1
    fi

    local rootdir=~/ohai.src/esa/grammar
    local start_rule=start

    if [ "$1" == "domain" ]
    then
	local grammar_name=AbstractDomain
	java_build=${rootdir}/abstract_domain/java/build
	if [ ! -z "$2" ];
	then
	    #inputfile=~/ohai.src/esa/abstract_domains/"$2"
	    inputfile=$(pwd)/"$2"
	else
	    inputfile=~/ohai.src/esa/abstract_domains/test.domain
	fi
    elif [ "$1" == "engine" ]
    then
	local grammar_name=Esl
	java_build=${rootdir}/engine_spec_lang/java/build
	if [ ! -z "$2" ];
	then
	    #inputfile=~/ohai.src/esa/engines/"$2"
	    inputfile=$(pwd)/"$2"
	else
	    inputfile=~/ohai.src/esa/engines/test.engine
	fi
    else
	echo "Usage: show_ast [domain | engine] [.domain file | .engine file (optional)]"
    fi

    if [ ! -d ${java_build} ]
    then
	echo [ERROR] Java class files do not exist!
	return 1
    fi

    cd ${java_build}
    grun ${grammar_name} ${start_rule} -gui ${inputfile}
    cd -
}

function usage {
   cat << EOF
Usage: antlrrc.sh - <application>

Performs some activity
EOF
   return 1
}
