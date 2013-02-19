' =============================================================================
' ==        WARNING THIS FILE IS GENERATED; DO NOT EDIT THIS FILE            ==
' =============================================================================

#IOS_BUNDLE_LABEL="{name[ios]}"
#IOS_BUNDLE_ID="{sku[ios]}"
#IOS_SCREEN_ORIENTATION="{orientation[ios]}"
#IOS_ACCELEROMETER_ENABLED=false
#IOS_DISPLAY_LINK_ENABLED=true
#IOS_RETINA_ENABLED=true

#GLFW_WINDOW_WIDTH=1024
#GLFW_WINDOW_HEIGHT=768

#BONO_ANDROID_MARKET="{args[vendor]}"
#COMMANDR_VENDOR="{args[vendor]}"

Const COMMANDR_GOOGLE_KEY := "{specials[google][key]}"
Const COMMANDR_IOS_ID := "{specials[ios][id]}"

#If COMMANDR_VENDOR="amazon"
    #ANDROID_APP_LABEL="{name[amazon]}"
    #ANDROID_APP_PACKAGE="{sku[amazon]}"
    #ANDROID_SCREEN_ORIENTATION="{orientation[amazon]}"

    Const COMMANDR_SKU := "{sku[amazon]}"
    Const COMMANDR_REVMOB_ID := "{specials[amazon][revmob]}"
#ElseIf COMMANDR_VENDOR="google"
    #ANDROID_APP_LABEL="{name[google]}"
    #ANDROID_APP_PACKAGE="{sku[google]}"
    #ANDROID_SCREEN_ORIENTATION="{orientation[google]}"

    Const COMMANDR_SKU := "{sku[google]}"
    Const COMMANDR_REVMOB_ID := "{specials[google][revmob]}"
#Else
    Const COMMANDR_SKU := "{sku[ios]}"
    Const COMMANDR_REVMOB_ID := "{specials[ios][revmob]}"
#End
