#!/bin/bash
echo "## " `date +"%Y-%m-%d, %H:%M:%S"` " : Start of pylon instances manager"

function serve {
    if [ "$5" != "" -a "$2" != "$5" ];
    then
        return
    fi
    cd $1
    #echo $1 $2 $3 $4 $5
    paster serve --daemon --pid-file=$1/config/$2.pid --log-file=$1/config/$2.log $1/config/$2.ini $4
}

for i in `cat /home/srv/urbanmap/urbanMap/config/pylon_instances.txt`
do
    #echo "Treating" $i
    path=`echo $i |cut -d';' -f1`
    inifile=`echo $i |cut -d';' -f2`
    port=`echo $i |cut -d';' -f3`
    
    case "$1" in
      start | stop | restart )
        serve $path $inifile $port $1 $2
        ;;
      *)
        echo $"Usage: $0 {start|stop|restart}, to act on all instances"
        echo $"Usage: $0 {start|stop|restart} inifile_without_extension, to act on one instance"
        exit 1
    esac
done

echo "## " `date +"%Y-%m-%d, %H:%M:%S"` " : End of pylon instances manager"