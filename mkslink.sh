if [ ! -d "$1" ]; then
    echo $1
    echo $2
    CMD //C "mklink /D $1 $2"
fi

