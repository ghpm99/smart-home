#!/bin/bash
cd $PROJECTS/smart-home/uwsgi
export LC_ALL=en_US.UTF8

start (){

      $PROJECTS/smart-home/.venv/bin/uwsgi --ini $PROJECTS/smart-home/uwsgi/uwsgi.ini;

}

stop () {

      $PROJECTS/smart-home/.venv/bin/uwsgi --stop $PROJECTS/smart-home/uwsgi/uwsgi.pid;
      sleep 5;
}

reload () {

      $PROJECTS/smart-home/.venv/bin/uwsgi --reload $PROJECTS/smart-home/uwsgi/uwsgi.pid;

}

log () {
    tail -f $PROJECTS/smart-home/log/error.log;
}

stats () {
    uwsgitop $PROJECTS/smart-home/uwsgi/stats.sock
}

### main logic ###
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart)
        stop
        start
        ;;
   reload)
        reload
        ;;
      log)
        log
        ;;
      stats)
        stats
        ;;



  *)
        echo $"Opções disponiveis: $0 {start|stop|reload|restart|log|stats}"
        exit 1
esac
exit 0
