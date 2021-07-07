# shellcheck shell=sh

CheckProcess() {
  if [ "$1" = "" ]; then
    return 1
  fi

  PROCESS_NUM=$(ps | grep "$1" | grep -v "grep" | wc -l)
  return $PROCESS_NUM
}

while [ 1 ]; do
  CheckProcess "/opt/bin/HtBoxMain"
  CheckRet=$?
  if [ $CheckRet -gt 1 ];  then
    killall -9 HtBoxMain
    exec /opt/bin/HtBoxMain &
  fi
  
  if [ $CheckRet -eq 0 ];  then              
    exec /opt/bin/HtBoxMain &      
  fi

  NewProNum=$(ls /opt/bin | grep "HtBoxMainUpdate" | wc -l)

  if [ $NewProNum -eq 1 ]; then
    killall -9 HtBoxMain
    mv /opt/bin/HtBoxMainUpdate /opt/bin/HtBoxMain
    chmod 111 /opt/bin/HtBoxMain
    sync
    exec /opt/bin/HtBoxMain &
  fi

  if ls /opt/bin/*.hbp 1>/dev/null 2>&1; then
    NetNewBin=$(ls /opt/bin/*.hbp -r | head -1)
    if [ $NetNewBin ]; then
      mv /opt/bin/$NetNewBin /opt/bin/HtBoxMainUpdate
    fi
  fi

  LogFileNum=$(ls /var/BoxMainAppLog | wc -l)
  if [ $LogFileNum -gt 10 ]; then
    rm_file=$(ls /var/BoxMainAppLog/*.log | head -1)
    rm $rm_file
  fi
  
  sleep 5
done
