# shellcheck shell=sh
NtpTimeTime=12
NtpTimeCnt=$NtpTimeTime
NetMonitorTmr=0
CheckProcess() {
  if [ "$1" = "" ]; then
    return 1
  fi

  PROCESS_NUM=$(ps | grep "$1" | grep -v "grep" | wc -l)

  if [ $PROCESS_NUM -eq 1 ]; then
    return 0
  else
    return 1
  fi
}

while [ 1 ]; do
  CheckProcess "HtBoxMain"
  CheckRet=$?
  if [ $CheckRet -eq 1 ]; then
    #killall -9 HtBoxMain
    ps | grep main_opc | grep -v grep | awk '{print $1}' | xargs kill -9
    exec ./HtBoxMain &
  fi

  CheckProcess "main_opc.py"
  CheckRet=$?
  if [ $CheckRet -eq 1 ]; then
    #killall -9 HtBoxMain
    python main_opc.py &
  fi

  NewProNum=$(ls | grep "HtBoxMainUpdate" | wc -l)

  if [ $NewProNum -eq 1 ]; then
    killall -9 HtBoxMain
    mv HtBoxMainUpdate HtBoxMain
    chmod 777 HtBoxMain
    exec ./HtBoxMain &
  fi

  if ls *.hb 1>/dev/null 2>&1; then
    NetNewBin=$(ls *.hb -r | head -1)
    if [ $NetNewBin ]; then
      mv $NetNewBin HtBoxMainUpdate
    fi
  fi

  LogFileNum=$(ls Log | wc -l)
  if [ $LogFileNum -gt 10 ]; then
    rm_file=$(ls Log/*.log | head -1)
    echo $rm_file
    rm $rm_file
  fi

  let "NtpTimeCnt+=1"
  if [ $NtpTimeCnt -gt $NtpTimeTime ]; then
    ntpdate 0.pool.ntp.org

    if [ "$?" == 0 ]; then
      echo "[ntp]: update done"
      NtpTimeTime=17280
      hwclock -w
    fi

    NtpTimeCnt=0

  fi

  let "NetMonitorTmr+=1"
  if [ $NetMonitorTmr -gt 60 ]; then
    echo "[net]:check route"
    python static_monitor.py
    NetMonitorTmr=0
  fi

  sleep 5
done
