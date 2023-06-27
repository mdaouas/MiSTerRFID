#!/bin/bash

rootPath="/media/fat/games/rfidLoader"

declare -A MGLargs
# [RBF]="Delay Type Index"
MGLargs[NES]="NES 2 f 1"
MGLargs[FDS]="NES 2 f 1"
MGLargs[NeoGeo]="NeoGeo 1 f 1"
MGLargs[Gameboy]="Gameboy 2 f 1"
MGLargs[TurboGrafx16CD]="TurboGrafx16 1 s 0"


core_loader()
{
    md5=($(echo -n $2 | shasum))
    if [ "$LASTUID" != "$3" ]
    then
        if [[ $1 = "Arcade" ]]
        then
            arcadeRBF="load_core /media/fat/_Arcade/$2"
            echo $arcadeRBF
            echo "${arcadeRBF}" > /dev/MiSTer_cmd
        else
            arguments=(${MGLargs[$1]})
            if [ -z "$arguments" ]
            then
                echo "core arguments for "$1" are missing loading aborted."
                exit 1
            fi
            if [ ! -f $rootPath/$md5.mgl ]
            then 
                echo "<mistergamedescription><rbf>_console/"${arguments[0]}"</rbf><file delay=\"${arguments[1]}\" type=\"${arguments[2]}\" index=\"${arguments[3]}\" path=\""$2"\"/></mistergamedescription>" > $rootPath/$md5.mgl
                echo $rootPath"/"$1"/"$md5".mgl write done."
            fi
            echo load_core $rootPath/$md5.mgl > /dev/MiSTer_cmd
        fi
        export LASTUID="$3"
    fi
}

core_loader $1 "$2" $3
